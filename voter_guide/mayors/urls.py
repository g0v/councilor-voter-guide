# -*- coding: utf-8 -*-
from django.conf.urls import url
from mayors import views

urlpatterns = [
    url(r'^info/(?P<mayor_id>\S+)/(?P<election_year>\d+)/$', views.info, name='info'),
    url(r'^suggestor/(?P<mayor_id>\S+)/(?P<election_year>\d+)/$', views.suggestor, name='suggestor'),
    url(r'^biller/(?P<mayor_id>\S+)/(?P<election_year>\d+)/$', views.biller, name='biller'),
    url(r'^pc/(?P<mayor_id>\S+)/$', views.pc, name='pc'),
]
