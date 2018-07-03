# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.db import connections, IntegrityError, transaction
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import Platforms, Platforms_Likes
from .forms import PlatformsForm
from candidates.forms import Intent_StandpointsForm
from candidates.models import Intent, Intent_Standpoints
from mayors.models import Terms as mayor_terms
from commontag.views import paginate


def lists(request):
    ref = {
        'create_at': 'id',
        'likes': 'likes'
    }
    order_by = ref.get(request.GET.get('order_by'), 'likes')
    qs = Q()
    if request.GET.get('type'):
        if request.GET['type'] == 'city':
            qs = Q(county__isnull=False)
        elif request.GET['type'] == 'candidates':
            qs = Q(intent__isnull=False) | Q(candidate__isnull=False)
        elif request.GET['type'] == 'councilors':
            qs = Q(councilor__isnull=False)
        elif request.GET['type'] == 'mayors':
            qs = Q(mayor__isnull=False)
    platforms = Platforms.objects.filter(qs).prefetch_related('intent_standpoints').order_by('-%s' % order_by)
    platforms = paginate(request, platforms, 12)
    return render(request, 'platforms/lists.html', {'platforms': platforms})

def detail(request, platform_id):
    platform = get_object_or_404(Platforms.objects.select_related('user'), uid=platform_id)
    intent = None
    if request.user.is_authenticated():
        user_liked = Platforms_Likes.objects.filter(platform_id=platform_id, user=request.user).exists()
        try:
            intent = Intent.objects.get(user=request.user)
        except:
            instance = None
        else:
            try:
                instance = Intent_Standpoints.objects.get(intent=intent, platform_id=platform_id)
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
                        intent_sp.platform = platform
                        intent_sp.save()
                else:
                    if request.POST.get('decision') == 'upvote' and not user_liked:
                        Platforms_Likes.objects.create(platform_id=platform_id, user=request.user)
                        platform.likes += + 1
                        platform.save(update_fields=["likes"])
                        user_liked = True
                    elif request.POST.get('decision') == 'downvote' and user_liked:
                        Platforms_Likes.objects.filter(platform_id=platform_id, user=request.user).delete()
                        platform.likes -= 1
                        platform.save(update_fields=["likes"])
                        user_liked = False

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
                            WHERE cis.platform_id = %s
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
        order by case
            when pro = true then 1
            else 2
        end, sum desc
        ) row
    ''', [platform.uid, platform.county])
    r = c.fetchone()
    intent_sp_of_platform = r[0] if r else []
    return render(request, 'platforms/detail.html', {'platform': platform, 'user_liked': request.user.is_authenticated and user_liked, 'intent_sp_of_platform': intent_sp_of_platform, 'intent': intent, 'form': intent and form})

@login_required
def propose(request):
    if request.method == 'GET':
        form = PlatformsForm()
        targets = {x: 1 for x in ['county', 'mayor', 'councilor', 'intent']}
        if request.GET.get('intent'):
            form.fields['intent'].initial = request.GET['intent']
            targets.pop('intent')
        elif request.GET.get('mayor'):
            form.fields['mayor'].initial = request.GET['mayor']
            targets.pop('mayor')
        elif request.GET.get('councilor'):
            form.fields['councilor'].initial = request.GET['councilor']
            targets.pop('councilor')
        else:
            targets.pop('county')
        for key in targets.keys():
            form.fields.pop(key)
        return render(request, 'platforms/propose.html', {'form': form})
    if request.method == 'POST':
        form = PlatformsForm(request.POST)
        if form.is_valid():
            platform = form.save(commit=False)
            platform.user = request.user
            platform.status = [{
                'status': 'create',
                'at': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
            }]
            platform.save()
            return redirect(reverse('platforms:lists'))
        else:
            return render(request, 'platforms/propose.html', {'form': form})
