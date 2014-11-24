from django.conf.urls import patterns, url
from bills import views

urlpatterns = patterns('',
    url(r'^(?P<county>)/(?P<index>normal)/$', views.select_county, name='bills'),
    url(r'^(?P<county>\S+)/(?P<index>normal)/$', views.bills, name='bills'),
    url(r'^(?P<county>\S+)/(?P<index>normal)/(?P<category>\S+)$', views.bills_category, name='bills_category'),
    url(r'^(?P<county>\S+)/(?P<bill_id>\S+)/$', views.bill_detail, name='bill_detail'),
)
