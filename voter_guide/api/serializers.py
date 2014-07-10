#from django.contrib.auth.models import User, Group
from rest_framework import serializers
from . import fields
from councilors.models import Councilors, CouncilorsDetail, Attendance
from votes.models import Votes, Councilors_Votes
from bills.models import Bills, Councilors_Bills
from sittings.models import Sittings


class Councilors_VotesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Councilors_Votes

class VotesSerializer(serializers.HyperlinkedModelSerializer):
    results = fields.Field()
    class Meta:
        model = Votes
        fields = ('uid', 'sitting', 'date', 'vote_seq', 'content', 'conflict', 'result', 'results')

class Councilors_BillsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Councilors_Bills

class BillsSerializer(serializers.HyperlinkedModelSerializer):
    param = fields.Field()
    class Meta:
        model = Bills

class AttendanceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Attendance

class SittingsSerializer(serializers.HyperlinkedModelSerializer):
    votes = VotesSerializer(many=True)
    class Meta:
        model = Sittings
        fields = ('uid', 'name', 'committee', 'date', 'ad', 'session', 'votes')

class CouncilorsDetailSerializer(serializers.HyperlinkedModelSerializer):
    contacts = fields.Field()
    term_end = fields.Field()
    links = fields.Field()
    social_media = fields.Field()
    param = fields.Field()
    class Meta:
        model = CouncilorsDetail

class CouncilorsSerializer(serializers.HyperlinkedModelSerializer):
    each_terms = CouncilorsDetailSerializer(many=True)
    class Meta:
        model = Councilors
