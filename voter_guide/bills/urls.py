from django.conf.urls import url
from bills import views

urlpatterns = [
    url(r'^detail/(?P<bill_id>\S+)/$', views.bill, name='bill'),
    url(r'^(?P<county>\S+)/$', views.bills, name='bills'),
]
