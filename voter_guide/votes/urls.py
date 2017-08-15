from django.conf.urls import url
from votes import views

urlpatterns = [
    url(r'^detail/(?P<vote_id>\S+)/$', views.vote, name='vote'),
    url(r'^(?P<county>\S+)/$', views.votes, name='votes'),
]
