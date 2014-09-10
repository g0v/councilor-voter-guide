# -*- coding: utf-8 -*-
from django.shortcuts import render
from .models import Candidates


def home1(request, county, election_year):
    candidates = Candidates.objects.filter(election_year=election_year, county=county).order_by('district', 'party')
    return render(request, 'candidates/home.html', {'election_year': election_year, 'county': county, 'candidates': candidates})

def districts(request, county, election_year):
    districts = Candidates.objects.filter(election_year=election_year, county=county).values('constituency', 'district').order_by('constituency').distinct()
    return render(request, 'candidates/districts.html', {'election_year': election_year, 'county': county, 'districts': districts})

def district(request, county, election_year, constituency):
    candidates = Candidates.objects.filter(election_year=election_year, county=county, constituency=constituency).order_by('party')
    return render(request, 'candidates/district.html', {'election_year': election_year, 'county': county, 'candidates': candidates})
