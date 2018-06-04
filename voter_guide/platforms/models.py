# -*- coding: utf-8 -*-
import uuid

from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import JSONField


class Platforms(models.Model):
    uid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    mayor = models.ForeignKey('mayors.terms', to_field='uid', blank=True, null=True, verbose_name=u'縣市長')
    councilor = models.ForeignKey('councilors.councilorsdetail', blank=True, null=True, verbose_name=u'縣市議員')
    candidate = models.ForeignKey('candidates.terms', to_field='uid', blank=True, null=True, verbose_name=u'候選人')
    intent = models.ForeignKey('candidates.intent', to_field='uid', blank=True, null=True, verbose_name=u'擬參選人')
    county = models.CharField(blank=True, null=True, db_index=True, max_length=100, verbose_name=u'縣市')
    content = models.TextField(verbose_name=u'願望')
    likes = models.IntegerField(db_index=True, default=0)
    references = JSONField(null=True)
    status = JSONField(null=True)

class Platforms_Likes(models.Model):
    platform = models.ForeignKey(Platforms, to_field='uid')
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    class Meta:
        unique_together = ('platform', 'user')
        index_together = ['platform', 'user']
