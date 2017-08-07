# -*- coding: utf-8 -*-
from django.conf.urls import url
from candidates import views
from voter_guide import views as voter_guide_views

urlpatterns = [
    url(r'^intents/(?P<election_year>\d+)$', views.intents, name='intents'),
    url(r'^(?P<election_year>\d+)/(?P<county>\S+)/(?P<constituency>\d+)/$', views.district, name='district'),
    url(r'^(?P<election_year>\d+)/(?P<county>\S+)/$', views.districts, name='districts'),
    url(r'^intent_home/$', views.intent_home, name='intent_home'),
    url(r'^intent_upsert/$', views.intent_upsert, name='intent_upsert'),
    url(r'^intent_detail/(?P<intent_id>\S+)/$', views.intent_detail, name='intent_detail'),
    url(r'^pc/(?P<candidate_id>\S+)/(?P<election_year>\d+)/$', views.pc, name='pc'),
    url(r'^\d+/$', voter_guide_views.select_county, {'category': 'candidates'}, name='select_county'),
    url(r'^(?P<county>\S+)/$', views.districts, {"election_year": '2014'}, name='candidates'),
]
