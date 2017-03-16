# -*- coding: utf-8 -*-
import operator
from re import compile as _Re
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.db.models import Count, Q

from councilors.models import CouncilorsDetail
from search.models import Keyword
from search.views import keyword_list, keyword_been_searched, keyword_normalize
from .models import Bills
from commontag.views import paginate

_unicode_chr_splitter = _Re( '(?s)((?:[\ud800-\udbff][\udc00-\udfff])|.)' ).split

def split_unicode_chrs( text ):
  return [ chr for chr in _unicode_chr_splitter( text ) if (chr!=' ' and chr) ]

def select_county(request, index, county):
    regions = [
        {"region": "北部", "counties": ["臺北市", "新北市", "桃園市", "基隆市", "宜蘭縣", "新竹縣", "新竹市"]},
        {"region": "中部", "counties": ["苗栗縣", "臺中市", "彰化縣", "雲林縣", "南投縣"]},
        {"region": "南部", "counties": ["嘉義縣", "嘉義市", "臺南市", "高雄市", "屏東縣"]},
        {"region": "東部", "counties": ["花蓮縣", "臺東縣"]},
        {"region": "離島", "counties": ["澎湖縣", "金門縣", "連江縣"]}
    ]
    return render(request, 'bills/select_county.html', {'index': index, 'regions': regions})


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
    bills = paginate(request, bills)

    district_list = list(set([i.district for i in CouncilorsDetail.objects.filter(county=county).filter(~Q(district=''))]))
    return render(request, 'bills/bills.html', {'county': county, 'index': index, 'keyword_hot': keyword_list('bills'), 'category':None, 'keyword': keyword, 'bills': bills, 'district_list': district_list})

def bills_category(request, county, index, category):
    query = Q(county=county, category=category)
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
    bills = paginate(request, bills)

    district_list = list(set([i.district for i in CouncilorsDetail.objects.filter(county=county).filter(~Q(district=''))]))
    return render(request, 'bills/bills.html', {'category':category, 'county': county, 'index': index, 'keyword_hot': keyword_list('bills'), 'keyword': keyword, 'bills': bills, 'district_list': district_list})

def bill_detail(request, county, bill_id):
    try:
        bill = Bills.objects.get(county=county, uid=bill_id)
    except Exception, e:
        print e
        return HttpResponseRedirect('/')
    return render(request, 'bills/bill_detail.html', {'county': county, 'bill': bill})
