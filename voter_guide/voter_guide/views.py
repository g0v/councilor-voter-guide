#-*- coding: UTF-8 -*-
from random import randint

from django.shortcuts import render, redirect
from django.urls import reverse

from bills.models import Bills
from commontag.views import coming_election_year


def select_county(request, category):
    regions = [
        {"region": "北部", "counties": ["臺北市", "新北市", "桃園市", "基隆市", "宜蘭縣", "新竹市", "新竹縣"]},
        {"region": "中部", "counties": ["臺中市", "苗栗縣", "彰化縣", "雲林縣", "南投縣"]},
        {"region": "南部", "counties": ["臺南市", "高雄市", "屏東縣", "嘉義縣", "嘉義市"]},
        {"region": "東部", "counties": ["花蓮縣", "臺東縣"]},
        {"region": "離島", "counties": ["澎湖縣", "金門縣", "連江縣"]}
    ]
    titles = {
        "candidates": "找候選人",
        "councilors": "找議員",
        "bills": "找提案",
        "votes": "找表決"
    }
    election_year = coming_election_year(None)
    return render(request, 'common/select_county.html', {'title': titles.get(category, ''), 'category': category, 'regions': regions, 'election_year': election_year})

def dispatch(request):
    count = Bills.objects.all().count()
    random_index = randint(0, count - 1)
    instance = Bills.objects.all()[random_index]
    return redirect(reverse('bills:bill_detail', kwargs={'county': instance.county, 'bill_id': instance.uid}))

def about(request):
    return render(request,'about.html', {})

def reference(request):
    return render(request,'reference.html', {})
