# -*- coding: utf-8 -*-
from django.conf.urls import url
from councilors import views

urlpatterns = [
    url(r'^(?P<index>conscience_vote|not_voting|bills|cs_attend)/(?P<county>\S+)/$', views.index, name='index'),
    url(r'^platform/(?P<councilor_id>\S+)/(?P<election_year>\d+)/$', views.platformer, name='platformer'),
    url(r'^sp/(?P<councilor_id>\S+)/(?P<election_year>\d+)/$', views.sp, name='sp'),
    url(r'^biller/(?P<councilor_id>\S+)/(?P<election_year>\d+)/$', views.biller, name='biller'),
    url(r'^biller_sp/(?P<councilor_id>\S+)/(?P<election_year>\d+)/$', views.biller_sp, name='biller_sp'),
    url(r'^voter/(?P<councilor_id>\S+)/(?P<election_year>\d+)/$', views.voter, name='voter'),
    url(r'^voter_sp/(?P<councilor_id>\S+)/(?P<election_year>\d+)/$', views.voter_sp, name='voter_sp'),
    url(r'^suggestor/(?P<councilor_id>\S+)/(?P<election_year>\d+)/$', views.suggestor, name='suggestor'),
    url(r'^info/(?P<councilor_id>\S+)/(?P<election_year>\d+)/$', views.info, name='info'),
    url(r'^pc/(?P<councilor_id>\S+)/$', views.pc, name='pc'),
    url(r'^(?P<county>\S+)/$', views.districts, name='councilors'),
]
