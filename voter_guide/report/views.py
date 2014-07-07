# -*- coding: utf-8 -*-
import operator
from django.shortcuts import render
from django.db.models import Count, Q
from .models import CouncilorsDetail
from bills.models import Bills


def biller_diversity(request, index, county, ad):
    basic_query = Q(ad=ad, county=county)
    param = {
        'biller_diversity': {
            'title': u'',
            'url_name': u'councilors:platformer',
            'tooltip': u'',
            'unit': u''
        }
    }
    if index == 'biller_diversity':
        councilors = Bills.objects.filter(basic_query)
        return render(request, 'councilors/index/index_ordered.html', {'param': param.get(index), 'ad': ad, 'county': county, 'no_count_list': no_count_list, 'councilors': councilors, 'compare': compare, 'index': index})
