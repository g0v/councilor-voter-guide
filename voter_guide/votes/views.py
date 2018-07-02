# -*- coding: utf-8 -*-
import operator
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.db.models import Q, F, Sum
from django.db import connections, IntegrityError, transaction

from .models import Votes, Councilors_Votes
from councilors.models import CouncilorsDetail
from candidates.models import Intent, Intent_Standpoints
from candidates.forms import Intent_StandpointsForm
from search.views import keyword_list, keyword_been_searched
from standpoints.models import Standpoints, User_Standpoint
from commontag.views import paginate
from bills.tasks import tag_create_achievement, tag_pro_achievement


def votes(request, county):
    qs = Q(sitting__county=county)
    if request.GET.get('has_tag') == 'yes':
        qs = qs & Q(uid__in=Standpoints.objects.exclude(vote__isnull=True).values_list('vote_id', flat=True).distinct())
    elif request.GET.get('has_tag') == 'no':
        qs = qs & ~Q(uid__in=Standpoints.objects.exclude(vote__isnull=True).values_list('vote_id', flat=True).distinct())
    if request.GET.get('tag'):
        vote_ids = Standpoints.objects.filter(county=county, title=request.GET['tag']).values_list('vote', flat=True)
        qs = qs & Q(uid__in=vote_ids)
    keyword = request.GET.get('keyword', '')
    if keyword:
        votes = Votes.objects.filter(qs & reduce(operator.and_, (Q(content__icontains=x) for x in keyword.split())))
        if votes:
            keyword_been_searched(keyword, 'votes', county)
    else:
        votes = Votes.objects.filter(qs)
    votes = votes.extra(
                     select={
                         'tags': "SELECT json_agg(row) FROM (SELECT title, pro FROM standpoints_standpoints su WHERE su.vote_id = votes_votes.uid ORDER BY su.pro DESC) row",
                     },
                 )\
                 .order_by('-date', 'vote_seq')
    votes = paginate(request, votes)
    standpoints = Standpoints.objects.filter(county=county, vote__isnull=False).values_list('title', flat=True).order_by('-pro').distinct()
    get_params = '&'.join(['%s=%s' % (x, request.GET[x]) for x in ['keyword', 'has_tag', 'tag'] if request.GET.get(x)])
    return render(request,'votes/votes.html', {'county': county, 'votes': votes, 'hot_keyword': keyword_list('votes', county), 'standpoints': standpoints, 'get_params': get_params})

def vote(request, vote_id):
    vote = get_object_or_404(Votes.objects.select_related('sitting'), uid=vote_id)
    intent = None
    if request.user.is_authenticated():
        try:
            intent = Intent.objects.get(user=request.user)
        except:
            instance = None
        else:
            try:
                instance = Intent_Standpoints.objects.get(intent=intent, vote_id=vote_id)
            except:
                instance = None
        if intent:
            form = Intent_StandpointsForm(instance=instance)
        if request.POST:
            with transaction.atomic():
                if request.POST.has_key('intent') and intent:
                    form = Intent_StandpointsForm(request.POST, instance=instance)
                    if form.has_changed() and form.is_valid():
                        intent_sp = form.save(commit=False)
                        intent_sp.intent = intent
                        intent_sp.vote = vote
                        intent_sp.save()
                else:
                    if request.POST.get('keyword', '').strip():
                        standpoint_id = u'vote-%s-%s' % (vote_id, request.POST['keyword'].strip())
                        standpoint, created = Standpoints.objects.get_or_create(uid=standpoint_id, county=vote.sitting.county, title=request.POST['keyword'].strip(), vote_id=vote_id, user=request.user)
                        if created:
                            User_Standpoint.objects.create(standpoint_id=standpoint_id, user=request.user)
                            Standpoints.objects.filter(uid=standpoint_id).update(pro=F('pro') + 1)
                            tag_create_achievement(request.user)
                            tag_pro_achievement(standpoint_id)
                    elif request.POST.get('pro'):
                        User_Standpoint.objects.create(standpoint_id=request.POST['pro'], user=request.user)
                        Standpoints.objects.filter(uid=request.POST['pro']).update(pro=F('pro') + 1)
                        tag_pro_achievement(request.POST['pro'])
                    elif request.POST.get('against'):
                        User_Standpoint.objects.get(standpoint_id=request.POST['against'], user=request.user).delete()
                        Standpoints.objects.filter(uid=request.POST['against']).update(pro=F('pro') - 1)

    c = connections['default'].cursor()
    c.execute(u'''
        select json_agg(row)
        from (
            select pro, json_agg(party_list) as party_list, sum(count)
            from (
                select pro, json_build_object('party', party, 'intents', intents, 'count', json_array_length(intents)) as party_list, json_array_length(intents) as count
                from (
                    select pro, party, json_agg(detail) as intents
                    from (
                        select pro, party, json_build_object('name', name, 'county', county, 'intent_id', intent_id, 'comment', comment) as detail
                        from (
                            select
                                cis.pro,
                                ci.party,
                                ci.name,
                                ci.county,
                                cis.intent_id,
                                cis.comment,
                                cis.create_at
                            FROM candidates_intent_standpoints cis
                            JOIN candidates_intent ci on ci.uid = cis.intent_id
                            WHERE cis.vote_id = %s
                            order by case
                                when ci.county = %s then 1
                                else 2
                            end, create_at
                        ) _
                    ) __
                    group by pro, party
                    order by pro, party
                ) ___
            ) ____
        group by pro
        order by sum desc
        ) row
    ''', [vote.uid, vote.sitting.county])
    r = c.fetchone()
    intent_sp_of_vote = r[0] if r else []
    standpoints_of_vote = Standpoints.objects.filter(vote_id=vote_id)\
                                             .order_by('-pro')
    if request.user.is_authenticated():
        standpoints_of_vote = standpoints_of_vote.extra(select={
            'have_voted': "SELECT true FROM standpoints_user_standpoint su WHERE su.standpoint_id = standpoints_standpoints.uid AND su.user_id = %s" % request.user.id,
        },)
    return render(request,'votes/vote.html', {'vote': vote, 'standpoints_of_vote': standpoints_of_vote, 'intent_sp_of_vote': intent_sp_of_vote, 'intent': intent, 'form': intent and form})
