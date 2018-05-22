# -*- coding: utf-8 -*-
from __future__ import unicode_literals


import operator
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.db import connections
from django.db.models import Count, Sum, Max, F, Q, Case, When, Value, IntegerField
from django.db.models.functions import Coalesce

from .models import Terms
from bills.models import Bills
from suggestions.models import Suggestions
from standpoints.models import Standpoints
from search.views import keyword_list, keyword_been_searched
from commontag.views import paginate


def biller(request, mayor_id, election_year):
    try:
        mayor = Terms.objects.get(election_year=election_year, mayor_id=mayor_id)
    except Exception, e:
        return HttpResponseRedirect('/')
    query = Q(mayors_bills__mayor_id=mayor.uid)
    if request.GET.get('has_tag') == 'yes':
        query = query & Q(uid__in=Standpoints.objects.exclude(bill__isnull=True).values_list('bill_id', flat=True).distinct())
    elif request.GET.get('has_tag') == 'no':
        query = query & ~Q(uid__in=Standpoints.objects.exclude(bill__isnull=True).values_list('bill_id', flat=True).distinct())
    query = query & Q(uid__in=Standpoints.objects.filter(title=request.GET['tag']).exclude(bill__isnull=True).values_list('bill_id', flat=True).distinct()) if request.GET.get('tag') else query
    keyword = request.GET.get('keyword', '')
    if keyword:
        bills = Bills.objects.filter(query & reduce(operator.and_, (Q(abstract__icontains=x) for x in keyword.split())))
        if bills:
            keyword_been_searched(keyword, 'bills', mayor.county)
    else:
        bills = Bills.objects.filter(query)
    bills = bills.extra(
                     select={
                         'tags': "SELECT json_agg(row) FROM (SELECT title, pro FROM standpoints_standpoints su WHERE su.bill_id = bills_bills.uid ORDER BY su.pro DESC) row",
                     },
                 )\
                 .order_by('-uid')
    bills = paginate(request, bills)
    get_params = '&'.join(['%s=%s' % (x, request.GET[x]) for x in ['keyword', ] if request.GET.get(x)])
    return render(request, 'mayors/biller.html', {'keyword_hot': keyword_list('bills', mayor.county), 'county': mayor.county, 'bills': bills, 'mayor': mayor, 'get_params': get_params})
