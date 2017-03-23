#from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import generics
from .serializers import *

from councilors.models import Councilors, CouncilorsDetail, Attendance
from votes.models import Votes, Councilors_Votes
from bills.models import Bills, Councilors_Bills
from candidates.models import Candidates
from sittings.models import Sittings
from suggestions.models import Suggestions, Councilors_Suggestions


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
    queryset = Candidates.objects.all().select_related('councilor')
    serializer_class = CandidatesSerializer
    filter_fields = ('councilor', 'last_election_year', 'election_year', 'name', 'birth', 'gender', 'party', 'title', 'constituency', 'county', 'district', 'votes', 'elected')

class SuggestionsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Suggestions.objects.all()
    serializer_class = SuggestionsSerializer
    filter_fields = ('uid', 'county', 'election_year', 'suggest_year', 'suggest_month', 'suggest_expense', 'approved_expense', 'district', 'constituency')

class Councilors_SuggestionsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Councilors_Suggestions.objects.all().select_related('suggestion', 'councilor')
    serializer_class = Councilors_SuggestionsSerializer
    filter_fields = ('councilor', 'suggestion', 'jurisdiction')
