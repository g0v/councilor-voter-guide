# -*- coding: utf-8 -*-
import operator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.db.models import Count, Q
from .models import Bills
from search.models import Keyword
from search.views import keyword_list, keyword_been_searched, keyword_normalize


def bills(request, county, index):
    query = Q(county=county)
    keyword = keyword_normalize(request.GET)
    if keyword:
        bills = Bills.objects.filter(query & reduce(operator.and_, (Q(abstract__icontains=x) for x in keyword.split()))).order_by('-uid')
        if bills:
            keyword_been_searched(keyword, 'bills')
    else:
        bills = Bills.objects.filter(query).order_by('-uid')
    return render(request, 'bills/bills.html', {'county': county, 'index': index, 'keyword_hot': keyword_list('bills'), 'keyword': keyword, 'bills': bills})

def bill_detail(request, county, bill_id):
    try:
        bill = Bills.objects.get(county=county, uid=bill_id)
    except Exception, e:
        print e
        return HttpResponseRedirect('/')
    return render(request, 'bills/bill_detail.html', {'county': county, 'bill': bill})
