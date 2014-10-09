# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from councilors import views

urlpatterns = patterns('',
    url(r'^(?P<index>conscience_vote|not_voting|bills|cs_attend|counties)/(?P<election_year>\d+)/(?P<county>)/$', views.select_county, name='index'),
    url(r'^(?P<index>conscience_vote|not_voting|bills|cs_attend|counties)/(?P<election_year>\d+)/(?P<county>\S+)/$', views.index, name='index'),
    url(r'^platform/(?P<councilor_id>\S+)/(?P<election_year>\d+)/$', views.platformer, name='platformer'),
    url(r'^biller/(?P<councilor_id>\S+)/(?P<election_year>\d+)/$', views.biller, name='biller'),
    url(r'^voter/(?P<councilor_id>\S+)/(?P<election_year>\d+)/$', views.voter, name='voter'),
    url(r'^suggestor/(?P<councilor_id>\S+)/(?P<election_year>\d+)/$', views.suggestor, name='suggestor'),
)
