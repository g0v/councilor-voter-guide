# -*- coding: utf-8 -*-
from django.shortcuts import render
from .models import Candidates


def counties(request, election_year):
    counties = Candidates.objects.filter(election_year=election_year).values_list('county', flat=True).order_by('county').distinct()
    return render(request, 'candidates/counties.html', {'election_year': election_year, 'counties': counties})

def districts(request, election_year, county):
    districts = Candidates.objects.filter(election_year=election_year, county=county).values('constituency', 'district').order_by('constituency').distinct()
    return render(request, 'candidates/districts.html', {'election_year': election_year, 'county': county, 'districts': districts})

def district(request, election_year, county, constituency):
    candidates = Candidates.objects.filter(election_year=election_year, county=county, constituency=constituency).order_by('party')
    return render(request, 'candidates/district.html', {'election_year': election_year, 'county': county, 'candidates': candidates})
