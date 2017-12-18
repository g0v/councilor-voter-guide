# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^achievements/$', views.achievements, name='achievements'),
]
