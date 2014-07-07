# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from report import views

urlpatterns = patterns('',
    url(r'^report/(?P<index>biller_diversity)/(?P<county>\S+)/(?P<ad>\d+)/$', views.biller_diversity, name='biller_diversity'),
)
