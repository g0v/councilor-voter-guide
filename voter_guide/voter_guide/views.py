#-*- coding: UTF-8 -*-
from random import randint

from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Q

from candidates.models import Terms
from bills.models import Bills
from votes.models import Votes
from standpoints.models import Standpoints
from commontag.views import coming_election_year


def home(request):
    election_year = coming_election_year(None)
    if request.GET.get('name'):
        try:
            candidate = Terms.objects.get(election_year=election_year, name=request.GET['name'])
            if candidate.type == 'mayors':
                return redirect(reverse('candidates:mayors', kwargs={'county': candidate.county})+u'?name=%s' % request.GET['name'])
            else:
                return redirect(reverse('candidates:district', kwargs={'county': candidate.county, 'constituency': candidate.constituency})+u'?name=%s' % request.GET['name'])
        except:
            pass
    return render(request, 'home.html')

def dispatch_bill(request, county=None):
    qs = Q(county=county) if county else Q()
    if request.GET.get('has_tag') == 'yes':
        qs = qs & Q(uid__in=Standpoints.objects.exclude(bill__isnull=True).values_list('bill_id', flat=True).distinct())
    count = Bills.objects.filter(qs).count()
    random_index = randint(0, count - 1)
    instance = Bills.objects.filter(qs)[random_index]
    return redirect(reverse('bills:bill', kwargs={'bill_id': instance.uid}))

def dispatch_vote(request, county=None):
    qs = Q(sitting__county=county) if county else Q()
    if request.GET.get('has_tag') == 'yes':
        qs = qs & Q(uid__in=Standpoints.objects.exclude(vote__isnull=True).values_list('vote_id', flat=True).distinct())
    count = Votes.objects.filter(qs).count()
    random_index = randint(0, count - 1)
    instance = Votes.objects.filter(qs)[random_index]
    return redirect(reverse('votes:vote', kwargs={'vote_id': instance.uid}))
