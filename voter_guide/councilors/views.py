# -*- coding: utf-8 -*-
import operator
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.db import connections
from django.db.models import Count, Sum, Q, Max

from .models import CouncilorsDetail, Attendance, PoliticalContributions
from votes.models import Votes, Councilors_Votes
from bills.models import Bills
from suggestions.models import Suggestions
from sittings.models import Sittings
from search.views import keyword_list, keyword_been_searched
from commontag.views import paginate


def districts(request, county):
    election_year = CouncilorsDetail.objects.filter(county=county).aggregate(Max('election_year'))['election_year__max']
    basic_query = Q(election_year=election_year, county=county, in_office=True)
    out_office = CouncilorsDetail.objects.filter(election_year=election_year, county=county, in_office=False)
    councilors = CouncilorsDetail.objects.filter(basic_query).order_by('district', 'party')
    return render(request, 'councilors/index/districts.html', {'election_year': election_year, 'county': county, 'councilors': councilors, 'out_office': out_office, 'index': 'districts'})

def index(request, index, county):
    election_year = CouncilorsDetail.objects.filter(county=county).aggregate(Max('election_year'))['election_year__max']
    basic_query = Q(election_year=election_year, county=county, in_office=True)
    out_office = CouncilorsDetail.objects.filter(election_year=election_year, county=county, in_office=False)
    param = {
        'cs_attend': {
            'title': u'議會開會缺席次數(多→少)',
            'url_name': u'councilors:platformer',
            'remark': u'attendance',
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
        councilors = CouncilorsDetail.objects.filter(basic_query & Q(attendance__category='CS', attendance__status='absent'))\
                                             .annotate(totalNum=Count('attendance__id'))\
                                             .order_by('-totalNum','party')\
                                             .extra(select={'compare': "SELECT COUNT(*) FROM councilors_attendance WHERE councilors_attendance.councilor_id = councilors_councilorsdetail.id AND councilors_attendance.category = 'CS' GROUP BY councilors_attendance.councilor_id"},)
        no_count_list = CouncilorsDetail.objects.filter(basic_query)\
                                                .exclude(councilor_id__in=councilors.values_list('councilor_id', flat=True))
        return render(request, 'councilors/index/index_ordered.html', {'param': param.get(index), 'election_year': election_year, 'county': county, 'no_count_list': no_count_list, 'councilors': councilors, 'out_office': out_office, 'index': index})
    if index == 'bills':
        query = basic_query & Q(councilors_bills__petition=False)
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

def info(request, councilor_id, election_year):
    try:
        councilor = CouncilorsDetail.objects.get(election_year=election_year, councilor_id=councilor_id)
    except Exception, e:
        return HttpResponseRedirect('/')
    return render(request, 'councilors/info.html', {'councilor': councilor})

def suggestor(request, councilor_id, election_year):
    q = dict(zip(['councilor_id', 'election_year'], [councilor_id, election_year]))
    try:
        councilor = CouncilorsDetail.objects.get(**q)
    except Exception, e:
        return HttpResponseRedirect('/')
    q = dict(zip(['election_year', 'councilors__councilor_id'], [election_year, councilor.id]))
    index = request.GET.get('index')
    suggestions_base = Suggestions.objects.filter(**q)
    total_expense = suggestions_base.aggregate(sum=Sum('approved_expense_avg'))
    if not index:
        suggestions = suggestions_base.values('bid_by')\
                                        .annotate(sum=Sum('approved_expense'), count=Count('uid'))\
                                        .order_by('-sum')
    elif index == u'rawdata':
        suggestions = suggestions_base.order_by('-uid')
        return render(request, 'councilors/suggestor.html', {'county': councilor.county, 'index': index, 'suggestions': list(suggestions), 'councilor': councilor, 'total_expense': total_expense})
    return render(request, 'councilors/suggestor.html', {'county': councilor.county, 'suggestions': list(suggestions), 'councilor': councilor, 'total_expense': total_expense})

def biller(request, councilor_id, election_year):
    try:
        councilor = CouncilorsDetail.objects.get(election_year=election_year, councilor_id=councilor_id)
    except Exception, e:
        return HttpResponseRedirect('/')
    query = Q(proposer__id=councilor.id, councilors_bills__petition=False)
    primaryonly = request.GET.get('primaryonly', False)
    if primaryonly:
        query = query & Q(councilors_bills__priproposer=True)
    keyword = request.GET.get('keyword', '')
    if keyword:
        bills = Bills.objects.filter(query & reduce(operator.and_, (Q(abstract__icontains=x) for x in keyword.split()))).order_by('-uid')
        if bills:
            keyword_been_searched(keyword, 'bills', councilor.county)
    else:
        bills = Bills.objects.filter(query).order_by('-uid')
    bills = paginate(request, bills)
    return render(request, 'councilors/biller.html', {'keyword_hot': keyword_list('bills', councilor.county), 'county': councilor.county, 'bills': bills, 'councilor': councilor, 'keyword': keyword, 'primaryonly': primaryonly, 'category':None, 'index':'councilor'})

def biller_category(request, councilor_id, election_year, category):
    try:
        councilor = CouncilorsDetail.objects.get(election_year=election_year, councilor_id=councilor_id)
    except Exception, e:
        return HttpResponseRedirect('/')
    query = Q(proposer__id=councilor.id, councilors_bills__petition=False, category=category)
    primaryonly = request.GET.get('primaryonly', False)
    if primaryonly:
        query = query & Q(councilors_bills__priproposer=True)
    keyword = request.GET.get('keyword', '')
    if keyword:
        bills = Bills.objects.filter(query & reduce(operator.and_, (Q(abstract__icontains=x) for x in keyword.split()))).order_by('-uid')
        if bills:
            keyword_been_searched(keyword, 'bills', councilor.county)
    else:
        bills = Bills.objects.filter(query).order_by('-uid')
    bills = paginate(request, bills)
    return render(request, 'councilors/biller.html', {'keyword_hot': keyword_list('bills', councilor.county), '`county': councilor.county, 'bills': bills, 'councilor': councilor, 'keyword': keyword, 'primaryonly': primaryonly, 'category':category})

def biller_sp(request, councilor_id, election_year):
    councilor = get_object_or_404(CouncilorsDetail.objects, election_year=election_year, councilor_id=councilor_id)
    terms_id = tuple(CouncilorsDetail.objects.filter(election_year__lte=election_year, councilor_id=councilor_id).values_list('id', flat=True))
    c = connections['default'].cursor()
    c.execute(u'''
        SELECT json_agg(row)
        FROM (
            SELECT
                CASE
                    WHEN priproposer = true AND petition = false THEN '主提案'
                    WHEN petition = false THEN '共同提案'
                    WHEN petition = true THEN '連署'
                END as role,
                s.title,
                count(*) as times,
                json_agg((select x from (select v.uid, v.abstract) x)) as bills
            FROM bills_councilors_bills lv
            JOIN standpoints_standpoints s on s.bill_id = lv.bill_id
            JOIN bills_bills v on lv.bill_id = v.uid
            WHERE lv.councilor_id in %s AND s.pro = (
                SELECT max(pro)
                FROM standpoints_standpoints ss
                WHERE ss.pro > 0 AND s.bill_id = ss.bill_id
                GROUP BY ss.bill_id
            )
            GROUP BY s.title, role
            ORDER BY role
        ) row
    ''', [terms_id])
    r = c.fetchone()
    standpoints = r[0] if r else []
    return render(request, 'councilors/biller_sp.html', {'councilor': councilor, 'standpoints': standpoints})

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
    keyword = request.GET.get('keyword', '')
    if keyword:
        votes = Councilors_Votes.objects.select_related().filter(query & reduce(operator.and_, (Q(vote__content__icontains=x) for x in keyword.split()))).order_by('-vote__date')
        if votes:
            keyword_been_searched(keyword, 'votes', councilor.county)
    else:
        votes = Councilors_Votes.objects.select_related().filter(query).order_by('-vote__date')
    vote_addup = votes.values('decision').annotate(totalNum=Count('vote', distinct=True)).order_by('-decision')
    votes = paginate(request, votes)
    return render(request,'councilors/voter.html', {'keyword_hot': keyword_list('votes', councilor.county), 'county': councilor.county, 'councilor': councilor, 'keyword': keyword, 'index': index, 'votes': votes, 'vote_addup': vote_addup, 'notvote': notvote})

def voter_sp(request, councilor_id, election_year):
    councilor = get_object_or_404(CouncilorsDetail.objects, election_year=election_year, councilor_id=councilor_id)
    terms_id = tuple(CouncilorsDetail.objects.filter(election_year__lte=election_year, councilor_id=councilor_id).values_list('id', flat=True))
    c = connections['default'].cursor()
    c.execute(u'''
        SELECT json_agg(row)
        FROM (
            SELECT
                CASE
                    WHEN lv.decision = 1 THEN '贊成'
                    WHEN lv.decision = -1 THEN '反對'
                    WHEN lv.decision = 0 THEN '棄權'
                    WHEN lv.decision isnull THEN '沒投票'
                END as decision,
                s.title,
                count(*) as times,
                json_agg((select x from (select v.uid, v.content) x)) as votes
            FROM votes_councilors_votes lv
            JOIN standpoints_standpoints s on s.vote_id = lv.vote_id
            JOIN votes_votes v on lv.vote_id = v.uid
            WHERE lv.councilor_id in %s AND s.pro = (
                SELECT max(pro)
                FROM standpoints_standpoints ss
                WHERE ss.pro > 0 AND s.vote_id = ss.vote_id
                GROUP BY ss.vote_id
            )
            GROUP BY s.title, lv.decision
            ORDER BY lv.decision
        ) row
    ''', [terms_id])
    r = c.fetchone()
    standpoints = r[0] if r else []
    return render(request, 'councilors/voter_sp.html', {'councilor': councilor, 'standpoints': standpoints})

def platformer(request, councilor_id, election_year):
    try:
        councilor = CouncilorsDetail.objects.get(election_year=election_year, councilor_id=councilor_id)
    except Exception, e:
        return HttpResponseRedirect('/')
    return render(request, 'councilors/platformer.html', {'county': councilor.county, 'councilor': councilor})
