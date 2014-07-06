# -*- coding: utf-8 -*-
import operator
from django.shortcuts import render
from django.db.models import Count, Q
from .models import CouncilorsDetail, Attendance
from bills.models import Bills
from sittings.models import Sittings
from search.views import keyword_list, keyword_been_searched, keyword_normalize


def index(request, index, county, ad):
    basic_query = Q(ad=ad, county=county)
    param = {
        'countys': {
            'title': u'%s - 依選區分組' % county,
            'url_name': u'councilors:biller'
        },
        'cs_attend': {
            'title': u'議會開會缺席次數(多→少)',
            'url_name': u'councilors:platformer',
            'tooltip': u'缺席',
            'unit': u'次'
        },
        'bills': {
            'title': u'議案數(多→少)',
            'url_name': u'councilors:biller',
            'tooltip': u'議案',
            'unit': u'個'
        }
    }
    if index == 'cs_attend':
        compare = Sittings.objects.filter(basic_query & Q(committee='')).count()
        councilors = CouncilorsDetail.objects.filter(basic_query & Q(in_office=True, attendance__category='CS', attendance__status='absent'))\
                                             .annotate(totalNum=Count('attendance__id'))\
                                             .order_by('-totalNum','party')
        no_count_list = CouncilorsDetail.objects.filter(basic_query)\
                                                .exclude(councilor_id__in=councilors.values_list('councilor_id', flat=True))
        return render(request, 'councilors/index/index_ordered.html', {'param': param.get(index), 'ad': ad, 'county': county, 'no_count_list': no_count_list, 'councilors': councilors, 'compare': compare, 'index': index})
    if index == 'bills':
        query = basic_query
        proposertype = False
        if 'proposertype' in request.GET:
            proposertype = request.GET['proposertype']
            if not proposertype: # only primary_proposer count
                query = query & Q(councilors_bills__priproposer=True)
        else: # no form submit
            query = query & Q(councilors_bills__priproposer=True)
        councilors = CouncilorsDetail.objects.filter(query)\
                                     .annotate(totalNum=Count('councilors_bills__id'))\
                                     .exclude(totalNum=0)\
                                     .order_by('-totalNum')
        no_count_list = CouncilorsDetail.objects.filter(basic_query)\
                                                .exclude(councilor_id__in=councilors.values_list('councilor_id', flat=True))
        return render(request, 'councilors/index/index_ordered.html', {'param': param.get(index), 'ad': ad, 'county': county, 'proposertype': proposertype, 'no_count_list': no_count_list, 'councilors': councilors, 'index': index})
    if index == 'countys':
        councilors = CouncilorsDetail.objects.filter(basic_query).order_by('district', 'party')
        return render(request, 'councilors/index/countys.html', {'param': param.get(index), 'ad': ad, 'county': county, 'councilors': councilors, 'index': index})

def biller(request, councilor_id, ad):
    proposertype = False
    try:
        councilor = CouncilorsDetail.objects.get(ad=ad, councilor_id=councilor_id)
    except Exception, e:
        return HttpResponseRedirect('/')
    query = Q(proposer__id=councilor.id)
    keyword = keyword_normalize(request.GET)
    if keyword:
        bills = Bills.objects.filter(query & reduce(operator.and_, (Q(abstract__icontains=x) for x in keyword.split()))).order_by('-uid')
        if bills:
            keyword_been_searched(keyword, 'bills')
    else:
        bills = Bills.objects.filter(query).order_by('-uid')
    return render(request, 'councilors/biller.html', {'keyword_hot': keyword_list('bills'), 'bills': bills, 'councilor': councilor, 'keyword': keyword, 'proposertype': proposertype, 'data': list(councilor.param)})

def platformer(request, councilor_id, ad):
    try:
        councilor = CouncilorsDetail.objects.get(ad=ad, councilor_id=councilor_id)
    except Exception, e:
        return HttpResponseRedirect('/')
    return render(request, 'councilors/platformer.html', {'councilor': councilor})
