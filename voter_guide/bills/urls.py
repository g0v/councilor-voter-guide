from django.conf.urls import url
from bills import views

urlpatterns = [
    url(r'^$', views.bills_area, {'category': 'councilors'}, name='bills_area'),
    url(r'^(?P<category>city_gov|councilors)/$', views.bills_area, name='bills_area'),
    url(r'^detail/(?P<bill_id>\S+)/$', views.bill, name='bill'),
    url(r'^(?P<category>city_gov|councilors)/(?P<county>\S+)/$', views.bills, name='bills'),
    url(r'^(?P<county>\S+)/$', views.bills, {'category': 'councilors'}, name='bills'),
]
