# -*- coding: utf-8 -*-
from django.conf.urls import url
from mayors import views

urlpatterns = [
    url(r'^biller/(?P<mayor_id>\S+)/(?P<election_year>\d+)/$', views.biller, name='biller'),
]
