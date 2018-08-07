#-*- coding: UTF-8 -*-
from random import randint

from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Q

from candidates.models import Terms, Intent
from bills.models import Bills
from votes.models import Votes
from standpoints.models import Standpoints
from commontag.views import paginate, coming_election_year


def home(request):
    election_year = coming_election_year(None)
    if request.GET.get('name'):
        try:
            candidate = Terms.objects.get(election_year=election_year, name=request.GET['name'])
            if candidate.type == 'mayors':
                return redirect(reverse('candidates:mayors', kwargs={'county': candidate.county})+u'?name=%s#%s' % (request.GET['name'], candidate.candidate_id))
            else:
                return redirect(reverse('candidates:district', kwargs={'county': candidate.county, 'constituency': candidate.constituency})+u'?name=%s#%s' % (request.GET['name'], candidate.candidate_id))
        except:
            candidate = Intent.objects.get(election_year=election_year, name=request.GET['name'])
            return redirect(reverse('candidates:district', kwargs={'county': candidate.county, 'constituency': candidate.constituency})+u'?intent=%s#%s' % (request.GET['name'], candidate.uid))
    return render(request, 'home.html')

def seemore(request):
    intents = Intent.objects.filter(election_year='2018').order_by('-likes')
    return render(request, 'seemore.html', {'intents': intents})

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
