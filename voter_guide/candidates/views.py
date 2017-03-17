# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.db.models import Count, Sum, Q
from .models import Candidates


def counties(request, election_year):
    regions = [
        {"region": "北部", "counties": ["臺北市", "新北市", "桃園市", "基隆市", "宜蘭縣", "新竹縣", "新竹市"]},
        {"region": "中部", "counties": ["苗栗縣", "臺中市", "彰化縣", "雲林縣", "南投縣"]},
        {"region": "南部", "counties": ["嘉義縣", "嘉義市", "臺南市", "高雄市", "屏東縣"]},
        {"region": "東部", "counties": ["花蓮縣", "臺東縣"]},
        {"region": "離島", "counties": ["澎湖縣", "金門縣", "連江縣"]}
    ]
    return render(request, 'candidates/counties.html', {'election_year': election_year, 'regions': regions})

def districts(request, election_year, county):
    districts = Candidates.objects.filter(election_year=election_year, county=county).values('constituency', 'district')\
                                  .annotate(candidates=Count('id'))\
                                  .order_by('constituency')
    return render(request, 'candidates/districts.html', {'election_year': election_year, 'county': county, 'districts': districts})

def district(request, election_year, county, constituency):
    candidates = Candidates.objects.filter(election_year=election_year, county=county, constituency=constituency).order_by('-votes')\
                                   .annotate(
                                       balance=Sum('councilor__each_terms__politicalcontributions__balance'),
                                       in_total=Sum('councilor__each_terms__politicalcontributions__in_total'),
                                       out_total=Sum('councilor__each_terms__politicalcontributions__out_total')
                                   )
    return render(request, 'candidates/district.html', {'election_year': election_year, 'county': county, 'candidates': candidates})
