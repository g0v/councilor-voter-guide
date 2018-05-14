# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField


class Mayors(models.Model):
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
    mayor = models.ForeignKey(Mayors, to_field='uid', related_name='each_terms')
    election_year = models.CharField(db_index=True, max_length=100)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=100, blank=True, null=True)
    party = models.CharField(db_index=True, max_length=100, blank=True, null=True)
    county = models.CharField(db_index=True, max_length=100)
    contact_details = JSONField(null=True)
    term_start = models.DateField(blank=True, null=True)
    term_end = JSONField(null=True)
    in_office = models.BooleanField(db_index=True)
    education = models.TextField(blank=True, null=True)
    experience = models.TextField(blank=True, null=True)
    remark = models.TextField(blank=True, null=True)
    image = models.URLField(blank=True, null=True)
    links = JSONField(null=True)
    social_media = JSONField(null=True)
    platform = models.TextField(blank=True, null=True)
    data = JSONField(null=True)
    class Meta:
        unique_together = ("mayor", "election_year")

    def __unicode__(self):
        return self.name
