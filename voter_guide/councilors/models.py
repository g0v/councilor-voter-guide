# -*- coding: utf-8 -*-
from django.db import models
from json_field import JSONField


class Attendance(models.Model):
    councilor = models.ForeignKey('councilors.CouncilorsDetail')
    sitting = models.ForeignKey('sittings.Sittings', to_field="uid")
    category = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    def __unicode__(self):
        return self.sitting

class FileLog(models.Model):
    sitting = models.CharField(unique=True, max_length=100)
    date = models.DateTimeField()
    def __unicode__(self):
        return self.sitting

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
    title = models.CharField(max_length=100, blank=True, null=True)
    constituency = models.CharField(max_length=100, blank=True, null=True)
    county = models.CharField(max_length=100)
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
    platform = models.TextField(blank=True, null=True)
    param = JSONField(null=True)
    def __unicode__(self):
        return self.name

    def _in_office_ad(self):
        return CouncilorsDetail.objects.filter(councilor_id=self.councilor_id).values_list('ad', flat=True).order_by('-ad')
    in_office_ad = property(_in_office_ad)

