# -*- coding: utf-8 -*-
import re
import random

from django.shortcuts import render
from django.db import connections
from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets, filters, generics, status
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from .serializers import *
from .forms import NameForm
from councilors.models import Councilors, CouncilorsDetail, Attendance
from votes.models import Votes, Councilors_Votes
from bills.models import Bills, Councilors_Bills
from candidates.models import Candidates, Terms
from elections.models import Elections
from sittings.models import Sittings
from suggestions.models import Suggestions, Councilors_Suggestions
from commontag.views import coming_election_year


def validateFields(d, fields):
    return [{field: 'This field is required.'} for field in fields if field not in d.keys()]

@api_view(['POST', ])
@csrf_exempt
@permission_classes((AllowAny, ))
@renderer_classes((JSONRenderer,))
def constituency(request):
    results = validateFields(request.data, ['type', 'county', 'district'])
    if results:     return Response(results, status=status.HTTP_400_BAD_REQUEST)
    d = request.data.copy()
    d['county'] = re.sub(u'台', u'臺', d['county'])
    coming_ele_year = coming_election_year(d['county'])
    constituencies = Elections.objects.get(id=coming_ele_year).data['constituencies']
    district = re.sub(u'[鄉鎮市區]$', '', d['district']) if not re.search(re.sub(u'[縣市]$', '', d['county']), d['district']) and len(d['district']) > 2 else d['district']
    for region in constituencies[d['county']]['regions']:
        if not region.get('villages') or not d.get('villages'):
            if district in region['districts_list']:
                d['constituency'] = region['constituency']
                break
        else:
            if d['villages'] in region['villages']:
                d['constituency'] = region['constituency']
                break
    return Response(d, status=status.HTTP_200_OK)

def GetCouncilorId(name):
    c = connections['default'].cursor()
    identifiers = {name, re.sub(u'[\w。˙・･•．.‧’〃\']', '', name), re.sub(u'\W', '', name).lower(), } - {''}
    if identifiers:
        c.execute('''
            SELECT uid
            FROM councilors_councilors
            WHERE identifiers ?| array[%s]
        ''' % ','.join(["'%s'" % x for x in identifiers]))
        r = c.fetchall()
        if r:
            return [x[0] for x in r]
    return []

def check_person_name(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            errors = []
            text = request.POST['content']
            text = text.strip(u'[　\s]')
            text = re.sub(u'(副?議長|議員)', '', text)
            text = re.sub(u'[　\n、]', u' ', text)
            text = re.sub(u'[ ]+(\d+)[ ]+', u'\g<1>', text)
            text = re.sub(u' ([^ \w]) ([^ \w]) ', u' \g<1>\g<2> ', text) # e.g. 楊　曜=>楊曜, 包含句首
            text = re.sub(u'^([^ \w]) ([^ \w]) ', u'\g<1>\g<2> ', text) # e.g. 楊　曜=>楊曜, 包含句首
            text = re.sub(u' ([^ \w]) ([^ \w])$', u' \g<1>\g<2>', text) # e.g. 楊　曜=>楊曜, 包含句尾
            text = re.sub(u' (\w+) (\w+) ', u' \g<1>\g<2> ', text) # e.g. Kolas Yotaka=>KolasYotaka, 包含句首
            text = re.sub(u'^(\w+) (\w+) ', u'\g<1>\g<2> ', text) # e.g. Kolas Yotaka=>KolasYotaka, 包含句首
            text = re.sub(u'　(\w+) (\w+)$', u' \g<1>\g<2>', text) # e.g. Kolas Yotaka=>KolasYotaka, 包含句尾
            text = re.sub(u'^([^ \w]) ([^ \w])$', u'\g<1>\g<2>', text) # e.g. 楊　曜=>楊曜, 單獨一人
            text = re.sub(u'^(\w+) (\w+)$', u'\g<1>\g<2>', text) # e.g. Kolas Yotaka=>KolasYotaka, 單獨一人
            for name in text.split():
                name = re.sub(u'(.*)[）)。】」]$', '\g<1>', name) # 名字後有標點符號
                if not GetCouncilorId(name):
                    errors.append(name)
            return render(request, 'api/check_person_name.html', {'form': form, 'errors': errors})
    else:
        form = NameForm()
    return render(request, 'api/check_person_name.html', {'form': form})

class CouncilorsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Councilors.objects.all().prefetch_related('each_terms')
    serializer_class = CouncilorsSerializer
    filter_fields = ('uid', 'name')

class CouncilorsDetailViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CouncilorsDetail.objects.all().select_related('councilor')
    serializer_class = CouncilorsDetailSerializer
    filter_fields = ('councilor', 'election_year', 'name', 'gender', 'party', 'title', 'constituency', 'county', 'in_office', 'term_start')

class AttendanceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Attendance.objects.all().select_related('sitting', 'councilor')
    serializer_class = AttendanceSerializer
    filter_fields = ('councilor', 'sitting', 'category', 'status')

class SittingsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Sittings.objects.all()
    serializer_class = SittingsSerializer
    filter_fields = ('uid', 'name', 'committee', 'date', 'election_year')

class VotesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Votes.objects.all().select_related('sitting')
    serializer_class = VotesSerializer
    filter_fields = ('voter', 'uid', 'sitting', 'date', 'vote_seq', 'content', 'result')

class Councilors_VotesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Councilors_Votes.objects.all().select_related('vote', 'councilor')
    serializer_class = Councilors_VotesSerializer
    filter_fields = ('councilor', 'vote', 'decision', 'conflict')

class BillsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Bills.objects.all().prefetch_related('proposer')
    serializer_class = BillsSerializer
    filter_fields = ('proposer', 'uid', 'county', 'type', 'category', 'last_action', 'bill_no', 'execution')

class Councilors_BillsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Councilors_Bills.objects.all().select_related('bill', 'councilor')
    serializer_class = Councilors_BillsSerializer
    filter_fields = ('councilor', 'bill', 'priproposer', 'petition')

class CandidatesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Candidates.objects.all().prefetch_related('each_terms')
    serializer_class = CandidatesSerializer
    filter_fields = ('name', 'birth')

class CandidatesTermsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Terms.objects.all().select_related('candidate')
    serializer_class = CandidatesTermsSerializer
    filter_fields = ('election_year', 'type', 'name', 'gender', 'party', 'constituency', 'county', 'district', 'votes', 'elected', 'occupy')

class SuggestionsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Suggestions.objects.all()
    serializer_class = SuggestionsSerializer
    filter_fields = ('uid', 'county', 'election_year', 'suggest_year', 'suggest_month', 'suggest_expense', 'approved_expense', 'district', 'constituency')

class Councilors_SuggestionsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Councilors_Suggestions.objects.all().select_related('suggestion', 'councilor')
    serializer_class = Councilors_SuggestionsSerializer
    filter_fields = ('councilor', 'suggestion', 'jurisdiction')
