# -*- coding: utf-8 -*-
from django.db import models
from json_field import JSONField


class Councilors(models.Model):
    uid = models.TextField(unique=True)
    name = models.CharField(max_length=100)
    birth = models.DateField(blank=True, null=True)
    former_names = models.CharField(max_length=100, blank=True, null=True)
    def __unicode__(self):
        return self.name

class CouncilorsDetail(models.Model):
    councilor = models.ForeignKey(Councilors, to_field="uid", related_name='each_terms')
    ad = models.IntegerField()
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=100, blank=True, null=True)
    party = models.CharField(max_length=100, blank=True, null=True)
    constituency = models.CharField(max_length=100)
    county = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    in_office = models.BooleanField()
    contacts = JSONField(null=True)
    term_start = models.DateField(blank=True, null=True)
    term_end = JSONField(null=True)
    education = models.TextField(blank=True, null=True)
    experience = models.TextField(blank=True, null=True)
    remark = models.TextField(blank=True, null=True)
    image = models.URLField(blank=True, null=True)
    links = JSONField(null=True)
    social_media = JSONField(null=True)
    hits = models.IntegerField()
    def __unicode__(self):
        return self.name
