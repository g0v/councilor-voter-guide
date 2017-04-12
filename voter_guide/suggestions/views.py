# -*- coding: utf-8 -*-
import urllib
import operator
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Sum, F, Q, Case, When, Value, IntegerField

from .models import Suggestions, Councilors_Suggestions
from councilors.models import CouncilorsDetail


def county_overview(request):
    suggestions = Suggestions.objects.all().prefetch_related('councilors__councilor')[:3]
    counties = Suggestions.objects.all()\
                        .values('county', 'suggest_year')\
                        .annotate(
                            sum=Sum('approved_expense'),
                            count=Count('uid'),
                            small_purchase=Sum(
                                Case(
                                    When(approved_expense__lte=100000, then=1),
                                    output_field=IntegerField(),
                                    default=Value(0)
                                )
                            ),
                        )\
                        .order_by('county', 'suggest_year')
    return render(request,'suggestions/county_overview.html', {'suggestions': suggestions, 'counties': counties})

def positions(request, county, order_by, option):
    args = Q(county=county, approved_expense__isnull=False)
    if option == 'no_district':
        args = args & Q(position__iregex=u'[^鄉鎮市區]$')
    positions = Suggestions.objects.filter(args)\
                  .values('suggest_year', 'position', )\
                  .annotate(
                      sum=Sum('approved_expense'),
                      count=Count('uid'),
                  )\
                  .order_by('suggest_year', '-%s' % order_by)
    return render(request,'suggestions/positions.html', {'county': county, 'positions': positions, 'order_by': order_by, 'option': option})

def each_year(request, county):
    years = Councilors_Suggestions.objects.filter(suggestion__county=county)\
                        .values('suggestion__suggest_year', 'councilor_id', 'councilor__name', 'councilor__title', 'councilor__party', 'councilor__councilor_id', 'councilor__election_year')\
                        .annotate(sum=Sum('suggestion__approved_expense_avg'), )\
                        .order_by('-suggestion__suggest_year', '-sum')
    return render(request,'suggestions/years.html', {'county': county, 'years': years})

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
