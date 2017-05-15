# -*- coding: utf-8 -*-
from django.conf.urls import url
from candidates import views

urlpatterns = [
    url(r'^(?P<election_year>\d+)/(?P<county>\S+)/(?P<constituency>\d+)/$', views.district, name='district'),
    url(r'^(?P<election_year>\d+)/(?P<county>\S+)/$', views.districts, name='districts'),
    url(r'^intent_home/$', views.intent_home, name='intent_home'),
    url(r'^intent_upsert/$', views.intent_upsert, name='intent_upsert'),
    url(r'^intent_detail/(?P<intent_id>\S+)/$', views.intent_detail, name='intent_detail'),
    url(r'^pc/(?P<candidate_id>\S+)/(?P<election_year>\d+)/$', views.pc, name='pc'),
    url(r'^(?P<county>\S+)/$', views.districts, {"election_year": '2014'}, name='candidates'),
]
