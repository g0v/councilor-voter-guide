#from django.contrib.auth.models import User, Group
from rest_framework import serializers
from councilors.models import Councilors, CouncilorsDetail, Attendance
from votes.models import Votes, Councilors_Votes
from bills.models import Bills, Councilors_Bills
from candidates.models import Candidates, Terms
from sittings.models import Sittings
from suggestions.models import Suggestions, Councilors_Suggestions


class Councilors_VotesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Councilors_Votes
        fields = '__all__'

class VotesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Votes
        fields = '__all__'
#       fields = ('uid', 'sitting', 'date', 'vote_seq', 'content', 'conflict', 'result', 'results')

class Councilors_BillsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Councilors_Bills
        fields = '__all__'

class BillsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Bills
        fields = '__all__'

class AttendanceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'

class SittingsSerializer(serializers.HyperlinkedModelSerializer):
    votes = VotesSerializer(many=True)
    class Meta:
        model = Sittings
        fields = '__all__'
#       fields = ('uid', 'name', 'committee', 'date', 'election_year', 'links')

class CouncilorsDetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CouncilorsDetail
        fields = '__all__'

class CouncilorsSerializer(serializers.HyperlinkedModelSerializer):
    each_terms = CouncilorsDetailSerializer(many=True)
    class Meta:
        model = Councilors
        fields = '__all__'

class CandidatesTermsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Terms
        fields = '__all__'

class CandidatesSerializer(serializers.HyperlinkedModelSerializer):
    each_terms = CandidatesTermsSerializer(many=True)
    class Meta:
        model = Candidates
        fields = '__all__'

class Councilors_SuggestionsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Councilors_Suggestions
        fields = '__all__'

class SuggestionsSerializer(serializers.HyperlinkedModelSerializer):
    councilors = Councilors_SuggestionsSerializer(many=True)
    class Meta:
        model = Suggestions
        fields = '__all__'
