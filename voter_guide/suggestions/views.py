# -*- coding: utf-8 -*-
import operator
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Sum, F, Q
from .models import Suggestions, Councilors_Suggestions
from councilors.models import CouncilorsDetail


def report(request):
    councilors = CouncilorsDetail.objects\
                           .filter(election_year='2010', county__in=[u'臺北市', u'高雄市'])\
                           .annotate(sum=Sum('suggestions__suggestion__approved_expense'), count=Count('suggestions__id'))\
                           .order_by('-sum')
    parties = CouncilorsDetail.objects\
                            .filter(election_year='2010', county__in=[u'臺北市', u'高雄市'])\
                            .values('party')\
                            .annotate(sum=Sum('suggestions__suggestion__approved_expense'), count=Count('suggestions__id'))\
                            .order_by('-sum')
    counties = CouncilorsDetail.objects\
                            .filter(election_year='2010', county__in=[u'臺北市', u'高雄市'])\
                            .values('county')\
                            .annotate(sum=Sum('suggestions__suggestion__approved_expense'), count=Count('suggestions__id'))\
                            .order_by('-sum')
    return render(request,'suggestions/report.html', {'councilors': councilors, 'parties': list(parties), 'counties': list(counties)})
