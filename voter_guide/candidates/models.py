# -*- coding: utf-8 -*-
from django.db import models
from json_field import JSONField
from councilors.models import CouncilorsDetail, Attendance
from votes.models import Councilors_Votes
from bills.models import Councilors_Bills


class Candidates(models.Model):
    councilor = models.ForeignKey('councilors.Councilors', to_field='uid', blank=True, null=True)
    last_election_year = models.CharField(db_index=True, max_length=100, blank=True, null=True)
    election_year = models.CharField(db_index=True, max_length=100)
    name = models.CharField(max_length=100)
    birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=100, blank=True, null=True)
    party = models.CharField(db_index=True, max_length=100, blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    constituency = models.IntegerField(db_index=True)
    county = models.CharField(db_index=True, max_length=100)
    district = models.CharField(db_index=True, max_length=100, blank=True, null=True)
    votes = models.IntegerField(blank=True, null=True)
    elected = models.NullBooleanField(db_index=True)
    contact_details = JSONField(null=True)
    education = models.TextField(blank=True, null=True)
    experience = models.TextField(blank=True, null=True)
    remark = models.TextField(blank=True, null=True)
    image = models.URLField(blank=True, null=True)
    links = JSONField(null=True)
    platform = models.TextField(blank=True, null=True)
    def __unicode__(self):
        return self.name

    def _not_vote_percentage(self):
        try:
            councilor = CouncilorsDetail.objects.get(councilor_id=self.councilor_id, election_year=self.last_election_year)
            if councilor.title == u'議長':
                return u'議長不參加表決'
        except Exception, e:
            return ''
        if Councilors_Votes.objects.filter(councilor_id=councilor.id):
            not_vote = Councilors_Votes.objects.filter(decision__isnull=True, councilor_id=councilor.id).count()
            should_vote = Councilors_Votes.objects.filter(councilor_id=councilor.id).count()
            return u'%.2f %% ' % (not_vote * 100.0 / should_vote)
        return u'沒有表決紀錄'
    pnotvote = property(_not_vote_percentage)

    def _conscience_vote_percentage(self):
        if self.last_election_year != '2010':
            return ''
        try:
            councilor = CouncilorsDetail.objects.get(councilor_id=self.councilor_id, election_year=self.last_election_year)
        except Exception, e:
            return ''
        if Councilors_Votes.objects.filter(councilor_id=councilor.id):
            not_vote = Councilors_Votes.objects.filter(conflict=True, councilor_id=councilor.id).count()
            should_vote = Councilors_Votes.objects.filter(councilor_id=councilor.id).count()
            return u'%.2f %% ' % (not_vote * 100.0 / should_vote)
        return u'沒有表決紀錄'
    pconsciencevote = property(_conscience_vote_percentage)

    def _pribiller_count(self):
        if self.last_election_year != '2010':
            return ''
        try:
            councilor = CouncilorsDetail.objects.get(councilor_id=self.councilor_id, election_year=self.last_election_year)
        except Exception, e:
            return ''
        return Councilors_Bills.objects.filter(councilor_id=councilor.id, priproposer=True).count()
    npribill = property(_pribiller_count)

    def _biller_count(self):
        if self.last_election_year != '2010':
            return ''
        try:
            councilor = CouncilorsDetail.objects.get(councilor_id=self.councilor_id, election_year=self.last_election_year)
        except Exception, e:
            return ''
        return Councilors_Bills.objects.filter(councilor_id=councilor.id, petition=False).count()
    nbill = property(_biller_count)

    def _term_end(self):
        try:
            councilor = CouncilorsDetail.objects.get(councilor_id=self.councilor_id, election_year=self.last_election_year)
        except Exception, e:
            return ''
        return councilor.term_end.get('date') if not councilor.in_office else None
    term_end = property(_term_end)

    def _cs_absent_count(self):
        try:
            councilor = CouncilorsDetail.objects.get(councilor_id=self.councilor_id, election_year=self.last_election_year)
            return Attendance.objects.filter(councilor_id=councilor.id, category='CS', status='absent').count()
        except Exception, e:
            return ''
    cs_absent = property(_cs_absent_count)
