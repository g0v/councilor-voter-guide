# -*- coding: utf-8 -*-
import operator
from django.shortcuts import render
from django.db.models import Count, Q
from .models import CouncilorsDetail, Attendance
from votes.models import Votes, Councilors_Votes
from bills.models import Bills
from sittings.models import Sittings
from search.views import keyword_list, keyword_been_searched, keyword_normalize


def select_county(request, index, election_year, county):
    counties = CouncilorsDetail.objects.filter(election_year=election_year).values_list('county', flat=True).order_by('county').distinct()
    return render(request, 'councilors/select_county.html', {'index': index, 'election_year': election_year, 'counties': counties})

def index(request, index, election_year, county):
    basic_query = Q(election_year=election_year, county=county, in_office=True)
    out_office = CouncilorsDetail.objects.filter(election_year=election_year, county=county, in_office=False)
    param = {
        'countys': {
            'title': u'%s - 依選區分組' % county
        },
        'cs_attend': {
            'title': u'議會開會缺席次數(多→少)',
            'url_name': u'councilors:platformer',
            'compare': u'缺席率',
            'tooltip': u'缺席',
            'unit': u'次'
        },
        'conscience_vote': {
            'title': u'脫黨投票次數(多→少)',
            'url_name': u"councilors:voter",
            'compare': u'脫黨投票率',
            'tooltip': u'脫黨投票',
            'unit': u'次'
        },
        'not_voting': {
            'title': u'表決缺席次數(多→少)',
            'url_name': u"councilors:voter",
            'compare': u'缺席率',
            'tooltip': u'表決缺席',
            'unit': u'次'
        },
        'bills': {
            'title': u'議案數(多→少)',
            'url_name': u'councilors:biller',
            'tooltip': u'議案',
            'unit': u'個'
        }
    }
    if index == 'conscience_vote':
        if not Votes.objects.filter(sitting__county=county):
            return render(request, 'councilors/index/index_ordered.html', {'param': param.get(index), 'election_year': election_year, 'county': county, 'no_count_list': None, 'councilors': None, 'out_office': out_office, 'index': index})
        councilors = CouncilorsDetail.objects.filter(basic_query, councilors_votes__conflict=True)\
                                     .annotate(totalNum=Count('councilors_votes__id'))\
                                     .order_by('-totalNum','party')\
                                     .extra(select={'compare': 'SELECT COUNT(*) FROM votes_councilors_votes WHERE votes_councilors_votes.councilor_id = councilors_councilorsdetail.id GROUP BY votes_councilors_votes.councilor_id'},)
        no_count_list = CouncilorsDetail.objects.filter(basic_query).exclude(councilor_id__in=councilors.values_list('councilor_id', flat=True)).order_by('party')
        return render(request, 'councilors/index/index_ordered.html', {'param': param.get(index), 'election_year': election_year, 'county': county, 'no_count_list': no_count_list, 'councilors': councilors, 'out_office': out_office, 'index': index})
    if index == 'not_voting':
        if not Votes.objects.filter(sitting__county=county):
            return render(request, 'councilors/index/index_ordered.html', {'param': param.get(index), 'election_year': election_year, 'county': county, 'no_count_list': None, 'councilors': None, 'out_office': out_office, 'index': index})
        councilors = CouncilorsDetail.objects.filter(basic_query, councilors_votes__decision__isnull=True)\
                                          .annotate(totalNum=Count('councilors_votes__id'))\
                                          .exclude(title='議長', totalNum=0)\
                                          .order_by('-totalNum','party')\
                                          .extra(select={'compare': 'SELECT COUNT(*) FROM votes_councilors_votes WHERE votes_councilors_votes.councilor_id = councilors_councilorsdetail.id GROUP BY votes_councilors_votes.councilor_id'},)
        no_count_list = CouncilorsDetail.objects.filter(basic_query).exclude(councilor_id__in=councilors.values_list('councilor_id', flat=True))
        return render(request, 'councilors/index/index_ordered.html', {'param': param.get(index), 'election_year': election_year, 'county': county, 'no_count_list': no_count_list, 'councilors': councilors, 'out_office': out_office, 'index': index})
    if index == 'cs_attend':
        if not Attendance.objects.filter(sitting__county=county):
            return render(request, 'councilors/index/index_ordered.html', {'param': param.get(index), 'election_year': election_year, 'county': county, 'no_count_list': None, 'councilors': None, 'out_office': out_office, 'index': index})
        compare = Sittings.objects.filter(election_year=election_year, county=county, committee='').count()
        councilors = CouncilorsDetail.objects.filter(basic_query & Q(attendance__category='CS', attendance__status='absent'))\
                                             .annotate(totalNum=Count('attendance__id'))\
                                             .order_by('-totalNum','party')
        no_count_list = CouncilorsDetail.objects.filter(basic_query)\
                                                .exclude(councilor_id__in=councilors.values_list('councilor_id', flat=True))
        return render(request, 'councilors/index/index_ordered.html', {'param': param.get(index), 'election_year': election_year, 'county': county, 'no_count_list': no_count_list, 'councilors': councilors, 'out_office': out_office, 'compare': compare, 'index': index})
    if index == 'bills':
        query = basic_query
        proposertype = False
        if 'proposertype' in request.GET:
            proposertype = request.GET['proposertype']
            if not proposertype: # only primary_proposer count
                query = query & Q(councilors_bills__priproposer=True)
        else: # no form submit
            query = query & Q(councilors_bills__priproposer=True)
        councilors = CouncilorsDetail.objects.filter(query)\
                                     .annotate(totalNum=Count('councilors_bills__id'))\
                                     .exclude(totalNum=0)\
                                     .order_by('-totalNum')
        no_count_list = CouncilorsDetail.objects.filter(basic_query)\
                                                .exclude(councilor_id__in=councilors.values_list('councilor_id', flat=True))
        return render(request, 'councilors/index/index_ordered.html', {'param': param.get(index), 'election_year': election_year, 'county': county, 'proposertype': proposertype, 'no_count_list': no_count_list, 'councilors': councilors, 'out_office': out_office, 'index': index})
    if index == 'counties':
        councilors = CouncilorsDetail.objects.filter(basic_query).order_by('district', 'party')
        return render(request, 'councilors/index/counties.html', {'param': param.get(index), 'election_year': election_year, 'county': county, 'councilors': councilors, 'out_office': out_office, 'index': index})

def biller(request, councilor_id, election_year):
    proposertype = False
    try:
        councilor = CouncilorsDetail.objects.get(election_year=election_year, councilor_id=councilor_id)
    except Exception, e:
        return HttpResponseRedirect('/')
    query = Q(proposer__id=councilor.id)
    keyword = keyword_normalize(request.GET)
    if keyword:
        bills = Bills.objects.filter(query & reduce(operator.and_, (Q(abstract__icontains=x) for x in keyword.split()))).order_by('-uid')
        if bills:
            keyword_been_searched(keyword, 'bills')
    else:
        bills = Bills.objects.filter(query).order_by('-uid')
    data = bills.values('category').annotate(totalNum=Count('id')).order_by('-totalNum')
    return render(request, 'councilors/biller.html', {'keyword_hot': keyword_list('bills'), 'county': councilor.county, 'bills': bills, 'councilor': councilor, 'keyword': keyword, 'proposertype': proposertype, 'data': list(data)})

def voter(request, councilor_id, election_year):
    votes, notvote, query = None, False, Q()
    try:
        councilor = CouncilorsDetail.objects.get(election_year=election_year, councilor_id=councilor_id)
    except Exception, e:
        return HttpResponseRedirect('/')
    #--> 依投票類型分類
    decision_query = {"agree": Q(decision=1), "disagree": Q(decision=-1), "abstain": Q(decision=0), "notvote": Q(decision__isnull=True)}
    if 'decision' in request.GET:
        decision = request.GET['decision']
        if decision_query.get(decision):
            query = decision_query.get(decision)
    #<--
    # 脫黨投票
    query = query & Q(councilor_id=councilor.id)
    index = 'normal'
    if 'index' in request.GET:
        index = request.GET['index']
        if index == 'conscience':
            query = query & Q(conflict=True)
    #<--
    keyword = keyword_normalize(request.GET)
    if keyword:
        votes = Councilors_Votes.objects.select_related().filter(query & reduce(operator.and_, (Q(vote__content__icontains=x) for x in keyword.split()))).order_by('-vote__date')
        if votes:
            keyword_been_searched(keyword, 'votes')
    else:
        votes = Councilors_Votes.objects.select_related().filter(query).order_by('-vote__date')
    vote_addup = votes.values('decision').annotate(totalNum=Count('vote', distinct=True)).order_by('-decision')
    return render(request,'councilors/voter.html', {'keyword_hot': keyword_list('votes'), 'county': councilor.county, 'councilor': councilor, 'keyword': keyword, 'index': index, 'votes': votes, 'vote_addup': vote_addup, 'notvote': notvote})

def platformer(request, councilor_id, election_year):
    try:
        councilor = CouncilorsDetail.objects.get(election_year=election_year, councilor_id=councilor_id)
    except Exception, e:
        return HttpResponseRedirect('/')
    return render(request, 'councilors/platformer.html', {'county': councilor.county, 'councilor': councilor})
