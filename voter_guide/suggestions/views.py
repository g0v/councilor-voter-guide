# -*- coding: utf-8 -*-
import urllib
import operator
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Sum, F, Q
from .models import Suggestions
from councilors.models import CouncilorsDetail


def county_overview(request):
    suggestions = Suggestions.objects.all()[:3]
    counties = Suggestions.objects.all()\
                        .values('county', 'suggest_year')\
                        .annotate(sum=Sum('approved_expense'), count=Count('uid'))\
                        .order_by('county', 'suggest_year')
    return render(request,'suggestions/county_overview.html', {'suggestions': suggestions, 'counties': list(counties)})

def report(request):
    councilors = CouncilorsDetail.objects.filter(election_year__in=['2009', '2010'], county__in=[u'臺北市', u'高雄市', u'新竹市']) | CouncilorsDetail.objects.filter(election_year__in=['2014'], county__in=[u'新北市', u'桃園市'])
    councilors = councilors.annotate(sum=Sum('suggestions__suggestion__approved_expense'), count=Count('suggestions__id'))\
                        .order_by('-sum')
    parties = councilors.values('party')\
                        .annotate(sum=Sum('suggestions__suggestion__approved_expense'), count=Count('suggestions__id'))\
                        .order_by('-sum')
    counties = Suggestions.objects.all()\
                        .values('county')\
                        .annotate(sum=Sum('approved_expense'), count=Count('uid'))\
                        .order_by('county')
    return render(request,'suggestions/report.html', {'councilors': councilors, 'parties': list(parties), 'counties': list(counties)})

def bid_by(request, bid_by):
    bid_by = urllib.unquote_plus(bid_by.encode('utf8'))
    councilors= CouncilorsDetail.objects.filter(suggestions__suggestion__bid_by__contains=[bid_by])
    parties = councilors.values('party')\
                    .annotate(sum=Sum('suggestions__suggestion__approved_expense'), count=Count('suggestions__suggestion'))\
                    .order_by('-sum')
    councilors = councilors.values('councilor_id', 'name', 'party', 'election_year')\
                    .annotate(sum=Sum('suggestions__suggestion__approved_expense'), count=Count('suggestions__suggestion'))\
                    .order_by('-sum')
    return render(request,'suggestions/bid_by.html', {'bid_by': bid_by, 'parties': list(parties), 'councilors': list(councilors)})
