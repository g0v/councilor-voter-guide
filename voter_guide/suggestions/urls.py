# -*- coding: utf-8 -*-
from django.conf.urls import url
from suggestions import views

urlpatterns = [
    url(r'^$', views.county_overview, name='county_overview'),
    url(r'^positions/(?P<county>\S+)/(?P<order_by>(sum|count))/(?P<option>\w+)/$', views.positions, name='positions'),
    url(r'^each_year/(?P<county>\S+)/$', views.each_year, name='each_year'),
    url(r'^bid_by/(?P<bid_by>.+)/$', views.bid_by, name='bid_by'),
]
