# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.postgres.fields import JSONField


class Achievements(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='achievements')
    name = models.CharField(max_length=100)
    checked = models.BooleanField(default=False, db_index=True)
    data = JSONField(null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('user', 'name')
        index_together = ['user', 'checked']

    def __unicode__(self):
        return self.name
