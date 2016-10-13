# -*- coding: utf-8 -*-
from django.conf.urls import url
from suggestions import views

urlpatterns = [
    url(r'^$', views.report, name='report'),
    url(r'^bid_by/(?P<bid_by>.+)/$', views.bid_by, name='bid_by'),
]
