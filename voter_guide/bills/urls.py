from django.conf.urls import url
from bills import views

urlpatterns = [
    url(r'^detail/(?P<county>\S+)/(?P<bill_id>\S+)/$', views.bill_detail, name='bill_detail'),
    url(r'^(?P<county>\S+)/(?P<index>normal)/$', views.bills, name='bills'),
    url(r'^(?P<county>\S+)/$', views.bills, {'index': 'normal'}, name='bills'),
    url(r'^(?P<county>\S+)/(?P<index>normal)/(?P<category>.+)$', views.bills_category, name='bills_category'),
]
