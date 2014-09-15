from django.conf.urls import patterns, url
from bills import views

urlpatterns = patterns('',
    url(r'^(?P<county>\S+)/(?P<index>normal)/$', views.bills, name='bills'),
    url(r'^(?P<county>\S+)/(?P<bill_id>\S+)/$', views.bill_detail, name='bill_detail'),
)
