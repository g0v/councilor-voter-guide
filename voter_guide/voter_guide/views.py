#-*- coding: UTF-8 -*-
from django.shortcuts import render


def select_county(request, category):
    regions = [
        {"region": "北部", "counties": ["臺北市", "新北市", "桃園市", "基隆市", "宜蘭縣", "新竹縣", "新竹市"]},
        {"region": "中部", "counties": ["苗栗縣", "臺中市", "彰化縣", "雲林縣", "南投縣"]},
        {"region": "南部", "counties": ["嘉義縣", "嘉義市", "臺南市", "高雄市", "屏東縣"]},
        {"region": "東部", "counties": ["花蓮縣", "臺東縣"]},
        {"region": "離島", "counties": ["澎湖縣", "金門縣", "連江縣"]}
    ]
    titles = {
        "candidates": "找候選人",
        "councilors": "找議員",
        "bills": "找議案",
        "votes": "找表決"
    }
    return render(request, 'common/select_county.html', {'title': titles.get(category, ''), 'category': category, 'regions': regions})

def about(request):
    return render(request,'about.html', {})

def reference(request):
    return render(request,'reference.html', {})
