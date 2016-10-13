# -*- coding: utf-8 -*-
from django.conf.urls import url
from candidates import views

urlpatterns = [
    url(r'^$', views.counties, {"election_year": '2014'}),
    url(r'^(?P<election_year>\d+)/(?P<county>\S+)/(?P<constituency>\d+)/$', views.district, name='district'),
    url(r'^(?P<election_year>\d+)/(?P<county>\S+)/$', views.districts, name='districts'),
    url(r'^(?P<election_year>\d+)/$', views.counties, name='counties'),
]
