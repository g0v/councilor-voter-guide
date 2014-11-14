# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.db.models import Count, Sum, Q
from .models import Candidates


def counties(request, election_year):
    counties = Candidates.objects.filter(election_year=election_year).values_list('county', flat=True).order_by('county').distinct()
    districts = []
    candidates = []
    for county in counties:
      data = Candidates.objects.filter(election_year=election_year, county=county).values('constituency', 'district').order_by('constituency')
      districts.append(data.distinct().count())
      candidates.append(data.count())
    
    hashList = zip(counties, districts, candidates)
    return render(request, 'candidates/counties.html', {'election_year': election_year, 'counties': counties, 'hashList': hashList})

def districts(request, election_year, county):
    districts = Candidates.objects.filter(election_year=election_year, county=county).values('constituency', 'district').order_by('constituency').distinct()
    candidates = []
    for constituency in range(1, len(districts)):
      candidates.append(Candidates.objects.filter(election_year=election_year, county=county, constituency=constituency).distinct().count())

    hashList = zip(districts, candidates)
    return render(request, 'candidates/districts.html', {'election_year': election_year, 'county': county, 'districts': districts, 'hashList': hashList})

def district(request, election_year, county, constituency):
    candidates = Candidates.objects.filter(election_year=election_year, county=county, constituency=constituency).order_by('party')\
                                   .annotate(
                                       balance=Sum('councilor__each_terms__politicalcontributions__balance'),
                                       in_total=Sum('councilor__each_terms__politicalcontributions__in_total'),
                                       out_total=Sum('councilor__each_terms__politicalcontributions__out_total')
                                    )
    return render(request, 'candidates/district.html', {'election_year': election_year, 'county': county, 'candidates': candidates})
