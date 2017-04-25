# -*- coding: utf-8 -*-
import operator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.db.models import Q

from .models import Votes, Councilors_Votes
from councilors.models import CouncilorsDetail
from search.views import keyword_list, keyword_been_searched
from commontag.views import paginate


def select_county(request, index, county):
    regions = [
        {"region": "北部", "counties": ["臺北市", "新北市", "桃園市", "基隆市", "宜蘭縣", "新竹縣", "新竹市"]},
        {"region": "中部", "counties": ["苗栗縣", "臺中市", "彰化縣", "雲林縣", "南投縣"]},
        {"region": "南部", "counties": ["嘉義縣", "嘉義市", "臺南市", "高雄市", "屏東縣"]},
        {"region": "東部", "counties": ["花蓮縣", "臺東縣"]},
        {"region": "離島", "counties": ["澎湖縣", "金門縣", "連江縣"]}
    ]
    return render(request, 'votes/select_county.html', {'index': index, 'regions': regions, 'category': 'votes'})

def votes(request, county, index='normal'):
    result = None
    if index == 'conscience':
        query = Q(sitting__county=county, conflict=True)
    else:
        query = Q(sitting__county=county)
    #--> 依表決結果分類
    if 'result' in request.GET:
        result = request.GET['result']
        query = query & Q(result=result)
    #<--
    keyword = request.GET.get('keyword', '')
    if keyword:
        votes = Votes.objects.filter(query & reduce(operator.and_, (Q(content__icontains=x) for x in keyword.split()))).order_by('-date', 'vote_seq')
        if votes:
            keyword_been_searched(keyword, 'votes')
    else:
        votes = Votes.objects.filter(query).order_by('-date', 'vote_seq')
    votes = paginate(request, votes)
    return render(request,'votes/votes.html', {'county': county, 'votes': votes, 'index':index, 'keyword':keyword, 'result':result, 'keyword_hot': keyword_list('votes')})

def vote(request, vote_id):
    data = None
    vote = Councilors_Votes.objects.select_related().filter(vote_id=vote_id).order_by('-decision', 'councilor__party')
    try:
        data = dict(Votes.objects.get(uid=vote_id).results)
        data.pop('total', None)
    except Exception, e:
        print e
        return HttpResponseRedirect('/')
    return render(request,'votes/vote.html', {'vote':vote, 'data':data})
