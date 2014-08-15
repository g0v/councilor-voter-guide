# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from councilors import views

urlpatterns = patterns('',
    url(r'^$', views.index, {"index": 'cs_attend', "county": u'臺北市', "election_year": '2010'}),
    url(r'^(?P<index>conscience_vote|not_voting|bills|cs_attend|countys)/(?P<county>\S+)/(?P<election_year>\d+)/$', views.index, name='index'),
    url(r'^platform/(?P<councilor_id>\S+)/(?P<election_year>\d+)/$', views.platformer, name='platformer'),
    url(r'^biller/(?P<councilor_id>\S+)/(?P<election_year>\d+)/$', views.biller, name='biller'),
    url(r'^voter/(?P<councilor_id>\S+)/(?P<election_year>\d+)/$', views.voter, name='voter'),
)
