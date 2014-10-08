# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from suggestions import views

urlpatterns = patterns('',
    url(r'^$', views.report, name='report'),
)
