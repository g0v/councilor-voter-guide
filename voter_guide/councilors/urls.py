# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from councilors import views

urlpatterns = patterns('',
    url(r'^$', views.index, {"index": 'cs_attend', "county": u'臺北市', "ad": 11}),
    url(r'^(?P<index>bills|cs_attend|countys)/(?P<county>\S+)/(?P<ad>\d+)/$', views.index, name='index'),
    url(r'^platform/(?P<councilor_id>\S+)/(?P<ad>\d+)/$', views.platformer, name='platformer'),
    url(r'^biller/(?P<councilor_id>\S+)/(?P<ad>\d+)/$', views.biller, name='biller'),
    #url(r'^report/(?P<index>cs_attend)/(?P<county>\S+)/(?P<ad>\d+)/$', views.chart_report, name='chart_report'),
)
