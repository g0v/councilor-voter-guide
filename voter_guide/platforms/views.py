# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import Platforms, Platforms_Likes
from .forms import PlatformsForm
from candidates.models import Intent
from mayors.models import Terms as mayor_terms
from commontag.views import paginate


def lists(request):
    ref = {
        'create_at': 'id',
        'likes': 'likes'
    }
    order_by = ref.get(request.GET.get('order_by'), 'likes')
    qs = Q(county=request.GET.get('county')) if request.GET.get('county') else Q()
    platforms = Platforms.objects.filter(qs).select_related('user').order_by('-%s' % order_by)
    platforms = paginate(request, platforms)
    return render(request, 'platforms/lists.html', {'platforms': platforms})

def detail(request, platform_id):
    platform = get_object_or_404(Platforms.objects.select_related('user'), uid=platform_id)
    if request.user.is_authenticated:
        user_liked = Platforms_Likes.objects.filter(platform_id=platform_id, user=request.user).exists()
        if request.method == 'POST':
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
    return render(request, 'platforms/detail.html', {'platform': platform, 'user_liked': request.user.is_authenticated and user_liked})

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
