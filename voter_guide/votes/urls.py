#-*- coding: UTF-8 -*-
from django.conf.urls import url
from votes import views

urlpatterns = [
    url(r'^detail/(?P<vote_id>\S+)/$', views.vote, name='vote'),
    url(r'^(?P<county>\S+)/$', views.votes, name='votes'),
    url(r'^$', views.votes, {'county': u'臺北市'}, name='votes'),
]
