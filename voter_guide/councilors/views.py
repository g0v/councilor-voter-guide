# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.db.models import Count, Q
from .models import CouncilorsDetail, Attendance
from sittings.models import Sittings


def index(request, index, county, ad):
    basic_query = Q(ad=ad, county=county)
    param = {
        'cs_attend': {
            'title': u'議會開會缺席次數(多→少)',
            'tooltip': u'缺席',
            'unit': u'次'
        },
        'bills': {
            'title': u'議案數(多→少)',
            'tooltip': u'議案',
            'unit': u'個'
        },
    }
    if index == 'cs_attend':
        compare = Sittings.objects.filter(basic_query & Q(committee='')).count()
        councilors = CouncilorsDetail.objects.filter(basic_query & Q(in_office=True, attendance__category='CS', attendance__status='absent'))\
                                             .annotate(totalNum=Count('attendance__id'))\
                                             .order_by('-totalNum','party')
        no_count_list = CouncilorsDetail.objects.filter(basic_query)\
                                                .exclude(councilor_id__in=councilors.values_list('councilor_id', flat=True))
        return render(request,'councilors/index/index_ordered.html', {'param': param.get(index), 'ad': ad, 'county': county, 'no_count_list': no_count_list, 'councilors': councilors, 'compare': compare, 'index': index})
    elif index == 'bills':
        proposertype = request.GET.get('proposertype', False)
        query = basic_query & Q(councilors_bills__priproposer=not proposertype)
        councilors = CouncilorsDetail.objects.filter(query)\
                                     .annotate(totalNum=Count('councilors_bills__id'))\
                                     .exclude(totalNum=0)\
                                     .order_by('-totalNum')
        no_count_list = CouncilorsDetail.objects.filter(basic_query)\
                                                .exclude(councilor_id__in=councilors.values_list('councilor_id', flat=True))
        return render(request,'councilors/index/index_ordered.html', {'param': param.get(index), 'ad': ad, 'county': county, 'proposertype': proposertype, 'no_count_list': no_count_list, 'councilors': councilors, 'index': index})

def platformer(request, councilor_id, ad):
    try:
        councilor = CouncilorsDetail.objects.get(ad=ad, councilor_id=councilor_id)
    except Exception, e:
        return HttpResponseRedirect('/')
    return render(request,'councilors/platformer.html', {'councilor':councilor})


