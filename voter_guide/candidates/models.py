# -*- coding: utf-8 -*-
import uuid

from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField, JSONField

from councilors.models import CouncilorsDetail, Attendance
from votes.models import Councilors_Votes
from bills.models import Bills, Councilors_Bills


class Candidates(models.Model):
    uid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    birth = models.DateField(blank=True, null=True)
    former_names = ArrayField(
        models.CharField(max_length=100),
        null=True,
        default=None,
    )
    identifiers = JSONField(null=True)
    def __unicode__(self):
        return self.name

class Terms(models.Model):
    uid = models.CharField(max_length=70, unique=True)
    candidate = models.ForeignKey(Candidates, to_field='uid')
    elected_councilor = models.OneToOneField('councilors.Councilorsdetail', blank=True, null=True, related_name='elected_candidate')
    councilor_terms = JSONField(null=True)
    election_year = models.CharField(db_index=True, max_length=100)
    number = models.IntegerField(db_index=True, blank=True, null=True)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=100, blank=True, null=True)
    party = models.CharField(db_index=True, max_length=100, blank=True, null=True)
    constituency = models.IntegerField(db_index=True)
    county = models.CharField(db_index=True, max_length=100)
    district = models.CharField(db_index=True, max_length=100, blank=True, null=True)
    votes = models.IntegerField(blank=True, null=True)
    votes_percentage = models.CharField(max_length=100, blank=True, null=True)
    elected = models.NullBooleanField(db_index=True)
    contact_details = JSONField(null=True)
    education = models.TextField(blank=True, null=True)
    experience = models.TextField(blank=True, null=True)
    remark = models.TextField(blank=True, null=True)
    image = models.URLField(blank=True, null=True)
    links = JSONField(null=True)
    platform = models.TextField(blank=True, null=True)
    politicalcontributions = JSONField(null=True)
    class Meta:
        unique_together = ("candidate", "election_year")
        index_together = ['election_year', 'county', 'constituency']

    def __unicode__(self):
        return self.name

class Intent(models.Model):
    uid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    candidate = models.ForeignKey(Candidates, to_field='uid', null=True)
    councilor_terms = JSONField(null=True)
    election_year = models.CharField(db_index=True, max_length=4, default='2018')
    likes = models.IntegerField(db_index=True, default=0)
    name = models.CharField(max_length=100, verbose_name=u'姓名')
    gender = models.CharField(max_length=100, blank=True, null=True, verbose_name=u'性別')
    party = models.CharField(db_index=True, max_length=100, verbose_name=u'政黨')
    constituency = models.PositiveIntegerField(db_index=True, verbose_name=u'選舉區')
    county = models.CharField(db_index=True, max_length=100, verbose_name=u'縣市')
    district = models.CharField(db_index=True, max_length=100, blank=True, null=True)
    contact_details = JSONField(null=True)
    education = models.TextField(blank=True, null=True, verbose_name=u'學歷')
    experience = models.TextField(blank=True, null=True, verbose_name=u'經歷')
    remark = models.TextField(blank=True, null=True, verbose_name=u'備註')
    links = JSONField(null=True)
    motivation = models.TextField(blank=True, null=True, verbose_name=u'為什麼報名')
    platform = models.TextField(blank=True, null=True, verbose_name=u'政見')
    politicalcontributions = JSONField(null=True)
    status = models.CharField(db_index=True, max_length=100)
    history = JSONField(null=True)
    class Meta:
        unique_together = ('user', 'election_year')
        index_together = ['election_year', 'county', 'constituency']

    def __unicode__(self):
        return self.name

class Intent_Likes(models.Model):
    intent = models.ForeignKey(Intent, to_field='uid')
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    class Meta:
        unique_together = ('intent', 'user')
        index_together = ['intent', 'user']
