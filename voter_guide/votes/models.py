# -*- coding: utf-8 -*-
from django.db import models
from json_field import JSONField


class Votes(models.Model):
    voter = models.ManyToManyField('councilors.CouncilorsDetail', through='Councilors_Votes')
    uid = models.CharField(max_length=110, unique=True)
    sitting = models.ForeignKey('sittings.Sittings', to_field="uid", related_name='votes')
    vote_seq = models.CharField(max_length=10)
    date = models.DateField()
    content = models.TextField()
    summary = models.TextField(blank=True, null=True)
    conflict = models.NullBooleanField()
    result = models.CharField(blank=True, null=True, max_length=50)
    results = JSONField(null=True)
    def __unicode__(self):
        return self.content

class Councilors_Votes(models.Model):
    councilor = models.ForeignKey('councilors.CouncilorsDetail')
    vote = models.ForeignKey(Votes, to_field="uid")
    decision = models.IntegerField(blank=True, null=True)
    conflict = models.NullBooleanField()
