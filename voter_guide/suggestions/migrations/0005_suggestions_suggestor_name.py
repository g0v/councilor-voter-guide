# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-18 10:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suggestions', '0004_auto_20170329_1349'),
    ]

    operations = [
        migrations.AddField(
            model_name='suggestions',
            name='suggestor_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
