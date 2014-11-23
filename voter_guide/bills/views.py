# -*- coding: utf-8 -*-
import operator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.db.models import Count, Q
from .models import Bills
from councilors.models import CouncilorsDetail
from search.models import Keyword
from search.views import keyword_list, keyword_been_searched, keyword_normalize
from re import compile as _Re

_unicode_chr_splitter = _Re( '(?s)((?:[\ud800-\udbff][\udc00-\udfff])|.)' ).split

def split_unicode_chrs( text ):
  return [ chr for chr in _unicode_chr_splitter( text ) if (chr!=' ' and chr) ]

def select_county(request, index, county):
    counties = CouncilorsDetail.objects.values_list('county', flat=True).order_by('county').distinct()
    return render(request, 'bills/select_county.html', {'index': index, 'counties': counties})

def bills(request, county, index):
    query = Q(county=county)
    keyword = keyword_normalize(request.GET)
    district = request.GET.get('district', None)


    if keyword:
        bills = Bills.objects.filter(query & reduce(operator.and_, (Q(abstract__icontains=x) for x in split_unicode_chrs(keyword))))
        if bills:
            keyword_been_searched(keyword, 'bills')
    else:
        bills = Bills.objects.filter(query)

    if district and district != 'all':
        all_councilor_id_in_district = list(set([i.id for i in CouncilorsDetail.objects.filter(county=county).filter(district__contains=district)]))
        bills = bills.filter(proposer__in=all_councilor_id_in_district)

    bills = bills.order_by('-uid')

    district_list = list(set([i.district for i in CouncilorsDetail.objects.filter(county=county).filter(~Q(district=''))]))
    return render(request, 'bills/bills.html', {'county': county, 'index': index, 'keyword_hot': keyword_list('bills'), 'keyword': keyword, 'bills': bills, 'district_list': district_list})

def bill_detail(request, county, bill_id):
    try:
        bill = Bills.objects.get(county=county, uid=bill_id)
    except Exception, e:
        print e
        return HttpResponseRedirect('/')
    return render(request, 'bills/bill_detail.html', {'county': county, 'bill': bill})
