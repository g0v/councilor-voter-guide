# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.db.models import Count, Q
from .models import CouncilorsDetail, Attendance
from sittings.models import Sittings


def index(request, index, county, ad):
    query = Q(ad=ad, county=county)
    param = {
        'cs_attend': {
            'title': u'議會開會缺席次數(多→少)'
        }
    }
    if index == 'cs_attend':
        compare = Sittings.objects.filter(query & Q(committee='')).count()
        councilors = CouncilorsDetail.objects.filter(query & Q(in_office=True, attendance__category='CS', attendance__status='absent')).annotate(totalNum=Count('attendance__id')).order_by('-totalNum','party')
        no_count_list = CouncilorsDetail.objects.filter(query).exclude(councilor_id__in=councilors.values_list('councilor_id', flat=True))
    return render(request,'councilors/index/index_ordered.html', {'param': param.get(index), 'ad': ad, 'county': county, 'no_count_list': no_count_list, 'councilors': councilors, 'index': index})

def platformer(request, councilor_id, ad):
    try:
        councilor = CouncilorsDetail.objects.get(ad=ad, councilor_id=councilor_id)
    except Exception, e:
        return HttpResponseRedirect('/')
    return render(request,'councilors/platformer.html', {'councilor':councilor})


