# -*- coding: utf-8 -*-
from django.conf.urls import url
from candidates import views

urlpatterns = [
    url(r'^(?P<election_year>\d+)/(?P<county>\S+)/(?P<constituency>\d+)/$', views.district, name='district'),
    url(r'^(?P<election_year>\d+)/(?P<county>\S+)/$', views.districts, name='districts'),
    url(r'^pc/(?P<candidate_id>\S+)/(?P<election_year>\d+)/$', views.pc, name='pc'),
    url(r'^(?P<county>\S+)/$', views.districts, {"election_year": '2014'}, name='candidates'),
]
