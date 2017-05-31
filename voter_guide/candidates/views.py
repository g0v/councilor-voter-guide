# -*- coding: utf-8 -*-
import json

from django.shortcuts import render, get_object_or_404, redirect
from django.db import connections
from django.db.models import Count, Sum, Q, F
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import Candidates, Terms, Intent, Intent_Likes
from .forms import IntentForm
from commontag.views import paginate


def intents(request, election_year):
    ref = {
        'create_at': 'id',
        'likes': 'likes'
    }
    order_by = ref.get(request.GET.get('order_by'), 'likes')
    intents = Intent.objects.filter(election_year=election_year).order_by('-%s' % order_by)
    intents = paginate(request, intents)
    return render(request, 'candidates/intents.html', {'intents': intents, 'election_year': election_year})

def districts(request, election_year, county):
    districts = Terms.objects.filter(election_year=election_year, county=county)\
                             .values('constituency', 'district')\
                             .annotate(candidates=Count('id'))\
                             .order_by('constituency')
    return render(request, 'candidates/districts.html', {'election_year': election_year, 'county': county, 'districts': districts})

def district(request, election_year, county, constituency):
    candidates = Terms.objects.filter(election_year=election_year, county=county, constituency=constituency).order_by('-votes')
    return render(request, 'candidates/district.html', {'election_year': election_year, 'county': county, 'district': candidates[0].district, 'candidates': candidates})

def intent_home(request):
    return render(request, 'candidates/intent_home.html', )

def intent_upsert(request):
    election_year = '2018'
    if not request.user.is_authenticated:
        return redirect(reverse('candidates:intent_home'))
    try:
        instance = Intent.objects.get(user=request.user, election_year=election_year)
    except:
        instance = None
    if request.method == 'GET':
        form = IntentForm(instance=instance)
        form.fields['name'].initial = request.user.last_name + request.user.first_name
    if request.method == 'POST':
        form = IntentForm(request.POST, instance=instance)
        if form.has_changed() and form.is_valid():
            intent = form.save(commit=False)
            intent.user = request.user
            intent.status = 'intent_apply'
            intent.save()
            c = connections['default'].cursor()
            history = request.POST.copy()
            history.pop('csrfmiddlewaretoken', None)
            history['modify_at'] = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
            c.execute('''
                UPDATE candidates_intent
                SET history = (%s::jsonb || COALESCE(history, '[]'::jsonb))
                WHERE user_id = %s AND election_year = %s
            ''', [json.dumps([history]), request.user.id, election_year])
        return redirect(reverse('candidates:intent_detail', kwargs={'intent_id': instance.uid if instance else intent.uid}))
    return render(request, 'candidates/intent_upsert.html', {'form': form})

def intent_detail(request, intent_id):
    intent = get_object_or_404(Intent.objects.select_related('user'), uid=intent_id)
    if request.user.is_authenticated:
        user_liked = Intent_Likes.objects.filter(intent_id=intent_id, user=request.user).exists()
        if request.method == 'POST':
            if request.POST.get('decision') == 'upvote' and not user_liked:
                Intent_Likes.objects.create(intent_id=intent_id, user=request.user)
                intent.likes += + 1
                intent.save(update_fields=["likes"])
                user_liked = True
            elif request.POST.get('decision') == 'downvote' and user_liked:
                Intent_Likes.objects.filter(intent_id=intent_id, user=request.user).delete()
                intent.likes -= 1
                intent.save(update_fields=["likes"])
                user_liked = False
    return render(request, 'candidates/intent_detail.html', {'intent': intent, 'user_liked': request.user.is_authenticated and user_liked})

def pc(request, candidate_id, election_year):
    candidate = get_object_or_404(Terms.objects, election_year=election_year, candidate_id=candidate_id)
    return render(request, 'candidates/pc.html', {'candidate': candidate})
