# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Sum, Q
from .models import Candidates, Terms


def districts(request, election_year, county):
    districts = Terms.objects.filter(election_year=election_year, county=county).values('constituency', 'district')\
                                  .annotate(candidates=Count('id'))\
                                  .order_by('constituency')
    return render(request, 'candidates/districts.html', {'election_year': election_year, 'county': county, 'districts': districts})

def district(request, election_year, county, constituency):
    candidates = Terms.objects.filter(election_year=election_year, county=county, constituency=constituency).order_by('-votes')
    return render(request, 'candidates/district.html', {'election_year': election_year, 'county': county, 'district': candidates[0].district, 'candidates': candidates})

def pc(request, candidate_id, election_year):
    candidate = get_object_or_404(Terms.objects, election_year=election_year, candidate_id=candidate_id)
#   pc = candidate.politicalcontributions
    return render(request, 'candidates/pc.html', {'candidate': candidate})
