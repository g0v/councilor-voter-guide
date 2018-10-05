#-*- coding: UTF-8 -*-
import re
import random
from random import randint

from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Q

from candidates.models import Terms, Intent, Candidates
from elections.models import Elections
from bills.models import Bills
from votes.models import Votes
from standpoints.models import Standpoints
from commontag.views import paginate, coming_election_year


def normalize_person_name(name):
    name_bk = name
    name = re.sub(u'(.+?\w+) (\w+)', u'\g<1>‧\g<2>', name) # e.g. Cemelesai Ljaljegan=>Cemelesai‧jaljegan
    if name != name_bk:
        print name
    name = re.sub(u'[。˙・･•．.-]', u'‧', name)
    name = re.sub(u'[　\s()（）’\'^]', '',name)
    name = name.title()
    return name

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
            try:
                name = normalize_person_name(request.GET['name'])
                identifiers = list({name, re.sub(u'[\w‧]', '', name), re.sub(u'\W', '', name).lower(), } - {''})
                candidate = Candidates.objects.get(identifiers__has_any_keys=identifiers)
                candidate = Terms.objects.get(election_year=election_year, candidate_id=candidate.uid)
                return redirect(reverse('candidates:district', kwargs={'county': candidate.county, 'constituency': candidate.constituency})+u'?name=%s#%s' % (candidate.name, candidate.candidate_id))
            except:
                pass
    return render(request, 'home.html')

def seemore(request):
    coming_ele_year = coming_election_year(None)
    try:
        election_config = Elections.objects.get(id=coming_ele_year).data
        referenda = election_config.get('referenda', [])
        random.shuffle(referenda)
    except:
        referenda = []
    return render(request, 'seemore.html', {'referenda': referenda})

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
