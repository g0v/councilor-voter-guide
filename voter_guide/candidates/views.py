# -*- coding: utf-8 -*-
import json

from django.shortcuts import render, get_object_or_404, redirect
from django.db import connections, transaction
from django.db.models import Count, Sum, Q, F
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import Candidates, Terms, Intent, Intent_Likes
from .forms import IntentForm, SponsorForm
from councilors.models import CouncilorsDetail
from platforms.models import Platforms
from elections.models import Elections
from commontag.views import paginate, coming_election_year
from .tasks import intent_register_achievement, intent_like_achievement


def intents(request, election_year):
    ref = {
        'create_at': 'id',
        'likes': 'likes'
    }
    order_by = ref.get(request.GET.get('order_by'), 'likes')
    qs = Q(county=request.GET.get('county')) if request.GET.get('county') else Q()
    qs = qs & Q(election_year=election_year)
    qs = qs & Q(constituency__in=request.GET.get('constituency').split(',')) if request.GET.get('constituency') else qs
    intents = Intent.objects.filter(qs).order_by('-%s' % order_by)
    intents = paginate(request, intents)
    intent_counties = Intent.objects.filter(qs).values('county').annotate(count=Count('county'))
    return render(request, 'candidates/intents.html', {'intents': intents, 'intent_counties': intent_counties, 'election_year': election_year})

def districts(request, election_year, county):
    coming_ele_year = coming_election_year(county)
    intents_count = Intent.objects.filter(election_year=coming_ele_year, county=county).count()
    districts = Terms.objects.filter(election_year=election_year, county=county)\
                             .values('constituency', 'district')\
                             .annotate(candidates=Count('id'))\
                             .order_by('constituency')
    return render(request, 'candidates/districts.html', {'coming_election_year': coming_ele_year, 'intents_count': intents_count, 'election_year': election_year, 'county': county, 'districts': districts})

def district(request, election_year, county, constituency):
    coming_ele_year = coming_election_year(county)
    transform_to_constiencies = []
    try:
        election_config = Elections.objects.get(id=coming_ele_year).data['constituency_change']
        for region in election_config.get(county, []):
            if constituency in region.get('from', {}).get('constituencies', []):
                transform_to_constiencies.append(region['constituency'])
    except:
        constiencies = [constituency]
    intents_count = Intent.objects.filter(election_year=coming_ele_year, county=county, constituency__in=transform_to_constiencies).count()
    candidates = Terms.objects.filter(election_year=election_year, county=county, constituency=constituency).order_by('-votes')
    standpoints = {}
    for term in [candidates]:
        for candidate in term:
            if candidate.councilor_terms:
                terms_id = tuple([x['term_id'] for x in candidate.councilor_terms])
                c = connections['default'].cursor()
                qs = u'''
                    SELECT jsonb_object_agg(k, v)
                    FROM (
                        SELECT 'votes' as k, json_agg(row) as v
                        FROM (
                            SELECT
                                CASE
                                    WHEN lv.decision = 1 THEN '贊成'
                                    WHEN lv.decision = -1 THEN '反對'
                                    WHEN lv.decision = 0 THEN '棄權'
                                    WHEN lv.decision isnull THEN '沒投票'
                                END as decision,
                                s.title,
                                count(*) as times,
                                sum(pro) as pro
                            FROM votes_councilors_votes lv
                            JOIN standpoints_standpoints s on s.vote_id = lv.vote_id
                            WHERE lv.councilor_id in %s AND s.pro = (
                                SELECT max(pro)
                                FROM standpoints_standpoints ss
                                WHERE ss.pro > 0 AND s.vote_id = ss.vote_id
                                GROUP BY ss.vote_id
                            )
                            GROUP BY s.title, lv.decision
                            ORDER BY pro DESC, times DESC
                            LIMIT 3
                        ) row
                        UNION ALL
                        SELECT 'bills' as k, json_agg(row) as v
                        FROM (
                            SELECT
                                s.title,
                                count(*) as times,
                                sum(pro) as pro
                            FROM bills_councilors_bills lv
                            JOIN standpoints_standpoints s on s.bill_id = lv.bill_id
                            JOIN bills_bills v on lv.bill_id = v.uid
                            WHERE lv.councilor_id in %s AND s.pro = (
                                SELECT max(pro)
                                FROM standpoints_standpoints ss
                                WHERE ss.pro > 0 AND s.bill_id = ss.bill_id
                                GROUP BY ss.bill_id
                            )
                            GROUP BY s.title
                            ORDER BY pro DESC, times DESC
                            LIMIT 3
                        ) row
                    ) r
                '''
                c.execute(qs, [terms_id, terms_id])
                r = c.fetchone()
                standpoints.update({candidate.id: r[0] if r else []})
    return render(request, 'candidates/district.html', {'coming_election_year': coming_ele_year, 'intents_count': intents_count, 'election_year': election_year, 'county': county, 'constituency': constituency, 'transform_to_constiencies': ','.join(transform_to_constiencies), 'district': candidates[0].district, 'candidates': candidates, 'standpoints': standpoints})

def intent_home(request):
    return render(request, 'candidates/intent_home.html', )

def intent_upsert(request):
    election_year = coming_election_year(None)
    if not request.user.is_authenticated:
        return redirect(reverse('candidates:intent_home'))
    try:
        instance = Intent.objects.get(user=request.user, election_year=election_year)
    except:
        instance = None
    if request.method == 'GET':
        form = IntentForm(instance=instance)
        form.fields['name'].initial = request.user.last_name + request.user.first_name
        form.fields['links'].initial = [{'note': u'Facebook 個人頁面', 'url': request.user.socialaccount_set.first().get_profile_url()}, None, None]
    if request.method == 'POST':
        form = IntentForm(request.POST, instance=instance)
        if form.has_changed() and form.is_valid():
            intent = form.save(commit=False)
            if intent.user_id and request.user.id != intent.user_id:
                return redirect(reverse('candidates:intent_home'))
            intent.user = request.user
            intent.status = 'intent_apply'
            intent.save()
            c = connections['default'].cursor()
            history = request.POST.copy()
            history.pop('csrfmiddlewaretoken', None)
            history['links'] = intent.links
            history['modify_at'] = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
            c.execute('''
                UPDATE candidates_intent
                SET history = (%s::jsonb || COALESCE(history, '[]'::jsonb))
                WHERE user_id = %s AND election_year = %s
            ''', [json.dumps([history]), request.user.id, election_year])
            intent_register_achievement(request.user)
        return redirect(reverse('candidates:intent_detail', kwargs={'intent_id': instance.uid if instance else intent.uid}))
    return render(request, 'candidates/intent_upsert.html', {'form': form})

def intent_detail(request, intent_id):
    intent = get_object_or_404(Intent.objects.select_related('user'), uid=intent_id)
    c = connections['default'].cursor()
    c.execute(u'''
        SELECT json_agg(row)
        FROM (
            SELECT
                cis.pro as decision,
                s.title,
                count(*) as times,
                sum(s.pro) as pro,
                json_agg((select x from (select v.uid, v.abstract) x)) as bills
            FROM candidates_intent_standpoints cis
            JOIN standpoints_standpoints s on s.bill_id = cis.bill_id
            JOIN bills_bills v on cis.bill_id = v.uid
            WHERE cis.intent_id = %s AND v.county = %s AND s.pro = (
                SELECT max(pro)
                FROM standpoints_standpoints ss
                WHERE ss.pro > 0 AND s.bill_id = ss.bill_id
                GROUP BY ss.bill_id
            )
            GROUP BY cis.pro, s.title
            ORDER BY decision, pro DESC
        ) row
    ''', [intent_id, intent.county])
    r = c.fetchone()
    standpoints = r[0] if r else []
    user_liked, form = False, None
    if request.user.is_authenticated:
        user_liked = Intent_Likes.objects.filter(intent_id=intent_id, user=request.user)
        if request.method == 'POST':
            if request.POST.get('decision') == 'upvote' and not user_liked:
                form = SponsorForm(request.POST)
                post = request.POST.dict()
                post.pop('csrfmiddlewaretoken', None)
                post['votable'] = {'1': u'未知', '2': u'是', '3': u'否', }.get(post['votable'])
                with transaction.atomic():
                    Intent_Likes.objects.create(intent_id=intent_id, user=request.user, data={'contact_details': post})
                    intent.likes += 1
                    intent.save(update_fields=['likes'])
                    user_liked = True
                intent_like_achievement(request.user, intent.likes > 99)
            elif request.POST.get('decision') == 'downvote' and user_liked:
                with transaction.atomic():
                    Intent_Likes.objects.filter(intent_id=intent_id, user=request.user).delete()
                    intent.likes -= 1
                    intent.save(update_fields=["likes"])
                    user_liked = False
        if not user_liked:
            form = SponsorForm()
            form.fields['name'].initial = request.user.last_name + request.user.first_name
            form.fields['email'].initial = request.user.email
    return render(request, 'candidates/intent_detail.html', {'form': form, 'intent': intent, 'standpoints': standpoints, 'user_liked': user_liked, 'is_this_intent': intent.user == request.user})

def intent_sponsor(request, intent_id):
    if not request.user.is_authenticated:
        return redirect(reverse('candidates:intent_detail', kwargs={'intent_id': intent_id}))
    intent = get_object_or_404(Intent.objects.select_related('user'), uid=intent_id, user=request.user)
    sponsors = Intent_Likes.objects.filter(intent_id=intent_id).order_by('-create_at')
    sponsors = paginate(request, sponsors)
    return render(request, 'candidates/intent_sponsor.html', {'sponsors': sponsors})

def pc(request, candidate_id, election_year):
    candidate = get_object_or_404(Terms.objects, election_year=election_year, candidate_id=candidate_id)
    return render(request, 'candidates/pc.html', {'candidate': candidate})
