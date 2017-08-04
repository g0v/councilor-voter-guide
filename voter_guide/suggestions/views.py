# -*- coding: utf-8 -*-
import re
import urllib
import operator
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Sum, F, Q, Case, When, Value, IntegerField
from django.conf import settings

from haystack.query import SearchQuerySet
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Suggestions, Councilors_Suggestions
from councilors.models import CouncilorsDetail
from search.views import keyword_list, keyword_been_searched
from commontag.views import paginate


def county_overview(request):
    qs = Q(content=request.GET['keyword']) if request.GET.get('keyword') else Q()
    suggestions = SearchQuerySet().filter(qs).models(Suggestions).order_by('-suggest_year')
    if qs and suggestions:
        keyword_been_searched(request.GET['keyword'], 'suggestions')
    try:
        page_size = int(request.GET.get('page_size', 3))
        page_size = 3 if page_size > 51 else page_size
    except:
        page_size = 3
    suggestions = paginate(request, suggestions, page_size)
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
    get_params = '&'.join(['%s=%s' % (x, request.GET[x]) for x in ['keyword'] if request.GET.get(x)])
    return render(request,'suggestions/county_overview.html', {'suggestions': suggestions, 'counties': counties, 'keyword': request.GET.get('keyword', ''), 'get_params': get_params})

def lists(request, county):
    qs = Q(county=county, content=request.GET['keyword']) if request.GET.get('keyword') else Q(county=county)
    suggestions = SearchQuerySet().filter(qs).models(Suggestions).order_by('-suggest_year')
    suggestions = paginate(request, suggestions)
    get_params = '&'.join(['%s=%s' % (x, request.GET[x]) for x in ['keyword'] if request.GET.get(x)])
    return render(request,'suggestions/lists.html', {'suggestions': suggestions, 'county': county, 'keyword': request.GET.get('keyword', ''), 'get_params': get_params})

def detail(request, uid):
    try:
        suggestion = SearchQuerySet().filter(uid=uid).models(Suggestions)[0]
    except:
        raise Http404
    if re.search(u'[鄉鎮市區里]$', suggestion.position):
        for p in [u'號', u'弄', u'巷']:
            address = re.sub(u'(.*?%s).*' % p, u'\g<1>', suggestion.suggestion)
            if len(address) != len(suggestion.suggestion):
                break
        address = re.sub(suggestion.position, '', address)
    else:
        address = ''
    address = '%s%s%s' % (suggestion.county, suggestion.position, address)
    return render(request,'suggestions/detail.html', {'suggestion': suggestion, 'address': address})

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
                  .order_by('-suggest_year', '-%s' % order_by)
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
