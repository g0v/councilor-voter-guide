# -*- coding: utf-8 -*-
from django.conf.urls import url
from candidates import views
from voter_guide import views as voter_guide_views

election_year = '2018'
urlpatterns = [
    url(r'^intents/(?P<election_year>\d+)/$', views.intents, name='intents'),
    url(r'^intent_home/$', views.intent_home, name='intent_home'),
    url(r'^intent_upsert/$', views.intent_upsert, name='intent_upsert'),
    url(r'^intent_detail/(?P<intent_id>\S+)/$', views.intent_detail, name='intent_detail'),
    url(r'^intent_sponsor/(?P<intent_id>\S+)/$', views.intent_sponsor, name='intent_sponsor'),
    url(r'^pc/(?P<candidate_id>\S+)/(?P<election_year>\d+)/$', views.pc, name='pc'),
    url(r'^mayors/(?P<county>\S+)/(?P<election_year>\d+)/$', views.mayors, name='mayors'),
    url(r'^mayors/(?P<county>\S+)/$', views.mayors, {'election_year': election_year}, name='mayors'),
    url(r'^mayors/$', views.mayors_area, {'election_year': election_year}, name='mayors_area'),
    url(r'^councilors/$', views.councilors_area, {'election_year': election_year}, name='councilors_area'),
    url(r'^councilors/(?P<county>\S+)/(?P<constituency>\d+)/(?P<election_year>\d+)/$', views.district, name='district'),
    url(r'^councilors/(?P<county>\S+)/(?P<constituency>\d+)/$', views.district, {'election_year': election_year}, name='district'),
    url(r'^councilors/(?P<county>\S+)/$', views.councilors_districts, {'election_year': election_year}, name='councilors_districts'),
    url(r'^user_generate_list/$', views.user_generate_list, name='user_generate_list'),
    url(r'^user_generated_list/(?P<list_id>\S+)/$', views.user_generated_list, name='user_generated_list'),
]
