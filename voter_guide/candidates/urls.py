# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from candidates import views

urlpatterns = patterns('',
    url(r'^$', views.districts, {"county": u'臺北市', "election_year": '2014'}),
    url(r'^(?P<election_year>\d+)/(?P<county>\S+)/(?P<constituency>\d+)/$', views.district, name='district'),
    url(r'^(?P<election_year>\d+)/(?P<county>\S+)/$', views.districts, name='districts'),
)
