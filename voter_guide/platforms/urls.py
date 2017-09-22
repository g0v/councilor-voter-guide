# -*- coding: utf-8 -*-
from django.conf.urls import url
from platforms import views

urlpatterns = [
    url(r'^lists/$', views.lists, name='lists'),
    url(r'^propose/$', views.propose, name='propose'),
    url(r'^detail/(?P<platform_id>\S+)/$', views.detail, name='detail'),
]
