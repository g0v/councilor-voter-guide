# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.postgres.fields import JSONField


class Attendance(models.Model):
    councilor = models.ForeignKey('councilors.CouncilorsDetail')
    sitting = models.ForeignKey('sittings.Sittings', to_field="uid")
    category = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    def __unicode__(self):
        return str(self.id)

class FileLog(models.Model):
    sitting = models.CharField(unique=True, max_length=100)
    date = models.DateTimeField()
    def __unicode__(self):
        return self.sitting

class Councilors(models.Model):
    uid = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=100)
    birth = models.DateField(blank=True, null=True)
    former_names = models.CharField(max_length=100, blank=True, null=True)
    identifiers = JSONField(null=True)
    data = JSONField(null=True)
    def __unicode__(self):
        return self.name

class CouncilorsDetail(models.Model):
    councilor = models.ForeignKey(Councilors, to_field="uid", related_name='each_terms')
    election_year = models.CharField(db_index=True, max_length=100)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=100, blank=True, null=True)
    party = models.CharField(db_index=True, max_length=100, blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    constituency = models.IntegerField(db_index=True, null=True)
    county = models.CharField(db_index=True, max_length=100)
    district = models.CharField(db_index=True, max_length=100, blank=True, null=True)
    in_office = models.BooleanField(db_index=True)
    contact_details = JSONField(null=True)
    term_start = models.DateField(blank=True, null=True)
    term_end = JSONField(null=True)
    education = models.TextField(blank=True, null=True)
    experience = models.TextField(blank=True, null=True)
    remark = models.TextField(blank=True, null=True)
    image = models.URLField(max_length=500, blank=True, null=True)
    links = JSONField(null=True)
    social_media = JSONField(null=True)
    platform = models.TextField(blank=True, null=True)
    param = JSONField(null=True)

    class Meta:
        unique_together = ("councilor", "election_year")

    def __unicode__(self):
        return self.name

    def _in_office_year(self):
        return CouncilorsDetail.objects.filter(councilor_id=self.councilor_id).values_list('election_year', flat=True).order_by('-election_year')
    in_office_year = property(_in_office_year)

class PoliticalContributions(models.Model):
    councilor = models.ForeignKey(CouncilorsDetail, related_name='politicalcontributions')
    in_individual = models.IntegerField(blank=True, null=True)
    in_profit = models.IntegerField(blank=True, null=True)
    in_party = models.IntegerField(blank=True, null=True)
    in_civil = models.IntegerField(blank=True, null=True)
    in_anonymous = models.IntegerField(blank=True, null=True)
    in_others = models.IntegerField(blank=True, null=True)
    in_total = models.IntegerField(blank=True, null=True)
    out_personnel = models.IntegerField(blank=True, null=True)
    out_propagate = models.IntegerField(blank=True, null=True)
    out_campaign_vehicle = models.IntegerField(blank=True, null=True)
    out_campaign_office = models.IntegerField(blank=True, null=True)
    out_rally = models.IntegerField(blank=True, null=True)
    out_travel = models.IntegerField(blank=True, null=True)
    out_miscellaneous = models.IntegerField(blank=True, null=True)
    out_return = models.IntegerField(blank=True, null=True)
    out_exchequer = models.IntegerField(blank=True, null=True)
    out_public_relation = models.IntegerField(blank=True, null=True)
    out_total = models.IntegerField(blank=True, null=True)
    balance = models.IntegerField(blank=True, null=True)
    def __unicode__(self):
        return self.balance
