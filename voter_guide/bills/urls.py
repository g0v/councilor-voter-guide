from django.conf.urls import url
from bills import views

urlpatterns = [
    url(r'^detail/(?P<county>\S+)/(?P<bill_id>\S+)/$', views.bill_detail, name='bill_detail'),
    url(r'^(?P<county>\S+)/$', views.bills, name='bills'),
]
