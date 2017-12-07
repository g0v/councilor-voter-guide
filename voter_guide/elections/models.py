# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.postgres.fields import JSONField


class Elections(models.Model):
    id = models.CharField(max_length=128, primary_key=True)
    data = JSONField()

    def __unicode__(self):
        return self.id
