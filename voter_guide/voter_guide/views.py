#-*- coding: UTF-8 -*-
from random import randint

from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Q

from bills.models import Bills
from votes.models import Votes
from standpoints.models import Standpoints
from commontag.views import coming_election_year


def select_county(request, category):
    regions = [
        {"region": "北部", "counties": ["臺北市", "新北市", "桃園市", "基隆市", "宜蘭縣", "新竹市", "新竹縣"]},
        {"region": "中部", "counties": ["臺中市", "苗栗縣", "彰化縣", "雲林縣", "南投縣"]},
        {"region": "南部", "counties": ["臺南市", "高雄市", "屏東縣", "嘉義縣", "嘉義市"]},
        {"region": "東部", "counties": ["花蓮縣", "臺東縣"]},
        {"region": "離島", "counties": ["澎湖縣", "金門縣", "連江縣"]}
    ] if category != 'votes' else [
        {"region": "北部", "counties": ["臺北市"]},
        {"region": "南部", "counties": ["高雄市"]},
    ]
    refs = {
        "candidates": {
            "title": "找候選人",
            "css_file": "css/councilmen.min.css",
            "page_id": "councilmen-area",
            "prefix_url": reverse('candidates:councilors_area')

        },
        "bills":  {
            "title": "找提案",
            "css_file": "css/bill.min.css",
            "page_id": "bill-area",
            "prefix_url": "/bills/"

        },
        "votes":  {
            "title": "找表決",
            "css_file": "css/councilmen.min.css",
            "page_id": "councilmen-area",
            "prefix_url": "/votes/"

        }
    }
    election_year = coming_election_year(None)
    return render(request, 'common/select_county.html', {'ref': refs.get(category, {}), 'category': category, 'election_year': election_year})

def dispatch_bill(request, county=None):
    qs = Q(county=county) if county else Q()
    if request.GET.get('has_tag') == 'yes':
        qs = qs & Q(uid__in=Standpoints.objects.exclude(bill__isnull=True).values_list('bill_id', flat=True).distinct())
    count = Bills.objects.filter(qs).count()
    random_index = randint(0, count - 1)
    instance = Bills.objects.filter(qs)[random_index]
    return redirect(reverse('bills:bill', kwargs={'bill_id': instance.uid}))

def dispatch_vote(request, county=None):
    qs = Q(sitting__county=county) if county else Q()
    if request.GET.get('has_tag') == 'yes':
        qs = qs & Q(uid__in=Standpoints.objects.exclude(vote__isnull=True).values_list('vote_id', flat=True).distinct())
    count = Votes.objects.filter(qs).count()
    random_index = randint(0, count - 1)
    instance = Votes.objects.filter(qs)[random_index]
    return redirect(reverse('votes:vote', kwargs={'vote_id': instance.uid}))

def about(request):
    return render(request,'about.html', {})

def reference(request):
    return render(request,'reference.html', {})
