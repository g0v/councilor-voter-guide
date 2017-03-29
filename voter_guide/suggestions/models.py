# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.postgres.fields import JSONField


class Suggestions(models.Model):
    uid = models.CharField(unique=True, db_index=True, max_length=100)
    county = models.CharField(db_index=True, max_length=100)
    election_year = models.CharField(db_index=True, max_length=4)
    suggest_year = models.CharField(max_length=4, db_index=True)
    suggest_month = models.CharField(max_length=2, db_index=True)
    suggestion = models.TextField()
    position = models.TextField(blank=True, null=True)
    suggest_expense = models.IntegerField(blank=True, null=True)
    suggest_expense_avg = models.IntegerField(blank=True, null=True)
    approved_expense = models.IntegerField(blank=True, null=True)
    approved_expense_avg = models.IntegerField(blank=True, null=True)
    expend_on = models.TextField(blank=True, null=True)
    brought_by = models.TextField(blank=True, null=True)
    bid_type = models.TextField(blank=True, null=True)
    bid_by = JSONField(null=True)
    district = models.CharField(db_index=True, max_length=100, blank=True, null=True)
    constituency = models.IntegerField(db_index=True, blank=True, null=True)
    def __unicode__(self):
        return self.uid

class Councilors_Suggestions(models.Model):
    councilor = models.ForeignKey('councilors.CouncilorsDetail', db_index=True, related_name='suggestions')
    suggestion = models.ForeignKey(Suggestions, to_field='uid', related_name='councilors')
    jurisdiction = models.NullBooleanField(db_index=True)

    class Meta:
        unique_together = ("councilor", "suggestion")
