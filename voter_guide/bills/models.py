# -*- coding: utf-8 -*-
from django.db import models
from json_field import JSONField


class Bills(models.Model):
    proposer = models.ManyToManyField('councilors.CouncilorsDetail', blank=True, null=True, through='Councilors_Bills')
    uid = models.TextField(unique=True)
    ad = models.IntegerField()
    county = models.CharField(max_length=100, blank=True, null=True)
    type = models.TextField(blank=True, null=True)
    category = models.TextField(blank=True, null=True)
    abstract = models.TextField(blank=True, null=True)
    last_action = models.TextField(blank=True, null=True)
    proposed_by = models.TextField(blank=True, null=True)
    committee = models.TextField(blank=True, null=True)
    resolusion_date = models.TextField(blank=True, null=True)
    resolusion_sitting = models.TextField(blank=True, null=True)
    resolusion = models.TextField(blank=True, null=True)
    bill_no = models.TextField(blank=True, null=True)
    intray_date = models.TextField(blank=True, null=True)
    intray_no = models.TextField(blank=True, null=True)
    receipt_date = models.TextField(blank=True, null=True)
    examination_date = models.TextField(blank=True, null=True)
    examination = models.TextField(blank=True, null=True)
    dispatch_no = models.TextField(blank=True, null=True)
    dispatch_date = models.TextField(blank=True, null=True)
    execution = models.TextField(blank=True, null=True)
    remark = models.TextField(blank=True, null=True)
    links = models.TextField(blank=True, null=True)
    param = JSONField(null=True)
    def __unicode__(self):
        return self.uid

    @property
    def sorted_proposer_set(self):
        return self.proposer.all().order_by('councilors_bills__id')

    @property
    def primary_proposer(self):
        return self.proposer.filter(councilors_bills__bill_id=self.uid, councilors_bills__priproposer=True)

class Councilors_Bills(models.Model):
    councilor = models.ForeignKey('councilors.CouncilorsDetail', blank=True, null=True)
    bill = models.ForeignKey(Bills, to_field='uid')
    priproposer = models.NullBooleanField()
    petition = models.NullBooleanField()
