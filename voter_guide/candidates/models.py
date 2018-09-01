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
    data = JSONField(null=True)
    def __unicode__(self):
        return self.name

class Terms(models.Model):
    uid = models.CharField(max_length=70, unique=True)
    type = models.CharField(db_index=True, max_length=20)
    candidate = models.ForeignKey(Candidates, to_field='uid', related_name='each_terms')
    elected_councilor = models.OneToOneField('councilors.Councilorsdetail', blank=True, null=True, related_name='elected_candidate')
    councilor_terms = JSONField(null=True)
    election_year = models.CharField(db_index=True, max_length=100)
    number = models.IntegerField(db_index=True, blank=True, null=True)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=100, blank=True, null=True)
    party = models.CharField(db_index=True, max_length=100, blank=True, null=True)
    constituency = models.IntegerField(db_index=True)
    county = models.CharField(db_index=True, max_length=100)
    district = models.TextField(db_index=True, blank=True, null=True)
    votes = models.IntegerField(blank=True, null=True)
    votes_percentage = models.CharField(max_length=100, blank=True, null=True)
    votes_detail = JSONField(null=True)
    elected = models.NullBooleanField(db_index=True)
    occupy = models.NullBooleanField(db_index=True)
    contact_details = JSONField(null=True)
    education = models.TextField(blank=True, null=True)
    experience = models.TextField(blank=True, null=True)
    remark = models.TextField(blank=True, null=True)
    image = models.URLField(blank=True, null=True)
    links = JSONField(null=True)
    platform = models.TextField(blank=True, null=True)
    politicalcontributions = JSONField(null=True)
    status = models.CharField(db_index=True, max_length=100)
    data = JSONField(null=True)
    class Meta:
        unique_together = ("candidate", "election_year")
        index_together = ['election_year', 'county', 'constituency']

    def __unicode__(self):
        return self.name

class Intent(models.Model):
    uid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    type = models.CharField(db_index=True, max_length=20, verbose_name=u'競選職位')
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    candidate = models.ForeignKey(Candidates, to_field='uid', null=True)
    candidate_term = models.OneToOneField(Terms, to_field='uid', blank=True, null=True, related_name='intent')
    councilor_terms = JSONField(null=True)
    election_year = models.CharField(db_index=True, max_length=4, default='2018')
    likes = models.IntegerField(db_index=True, default=0)
    name = models.CharField(max_length=100, verbose_name=u'姓名')
    slogan = models.CharField(max_length=20, blank=True, null=True, verbose_name=u'標語')
    gender = models.CharField(max_length=100, blank=True, null=True, verbose_name=u'性別')
    party = models.CharField(db_index=True, max_length=100, verbose_name=u'政黨')
    constituency = models.IntegerField(db_index=True, verbose_name=u'選舉區')
    county = models.CharField(db_index=True, max_length=100, verbose_name=u'縣市')
    district = models.TextField(db_index=True, blank=True, null=True)
    contact_details = JSONField(null=True)
    education = models.TextField(blank=True, null=True, verbose_name=u'學歷')
    experience = models.TextField(blank=True, null=True, verbose_name=u'經歷')
    remark = models.TextField(blank=True, null=True, verbose_name=u'備註')
    links = JSONField(blank=True, null=True, verbose_name=u'網站')
    video_link = models.URLField(blank=True, null=True, verbose_name=u'影片')
    motivation = models.TextField(blank=True, null=True, verbose_name=u'為何參選')
    platform = models.TextField(blank=True, null=True, verbose_name=u'地方政見')
    ideology = models.TextField(blank=True, null=True, verbose_name=u'政治理念')
    politicalcontributions = JSONField(null=True)
    status = models.CharField(db_index=True, max_length=100)
    history = JSONField(null=True)
    data = JSONField(null=True)
    class Meta:
        unique_together = ('user', 'election_year')
        index_together = ['election_year', 'county', 'constituency']

    def __unicode__(self):
        return self.name

class Intent_Likes(models.Model):
    intent = models.ForeignKey(Intent, to_field='uid')
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    create_at = models.DateTimeField(db_index=True, auto_now_add=True, null=True)
    data = JSONField(null=True)
    class Meta:
        unique_together = ('intent', 'user')
        index_together = ['intent', 'user']

class Intent_Standpoints(models.Model):
    intent = models.ForeignKey(Intent, to_field='uid')
    pro = models.BooleanField(db_index=True, verbose_name=u'贊成')
    comment = models.TextField(blank=True, null=True, verbose_name=u'意見')
    vote = models.ForeignKey('votes.Votes', to_field='uid', related_name='intent_standpoints', null=True)
    bill = models.ForeignKey('bills.Bills', to_field='uid', related_name='intent_standpoints', null=True)
    suggestion = models.ForeignKey('suggestions.Suggestions', to_field='uid', related_name='intent_standpoints', null=True)
    platform = models.ForeignKey('platforms.Platforms', to_field='uid', related_name='intent_standpoints', null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    data = JSONField(null=True)
    def __unicode__(self):
        return self.intent

class User_Generate_List(models.Model):
    uid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    content = models.TextField(blank=True, null=True, verbose_name=u'候選人名字')
    recommend = models.NullBooleanField(db_index=True, verbose_name=u'您推薦這份名單？')
    link = models.URLField(blank=True, null=True, verbose_name=u'外部網址')
    publish = models.BooleanField(default=False, db_index=True)
    create_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)
    data = JSONField(null=True)
