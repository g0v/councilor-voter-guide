from django.conf.urls import url
from votes import views

urlpatterns = [
    url(r'^(?P<county>\S+)/(?P<index>normal|conscience)/$', views.votes, name='votes'),
    url(r'^(?P<county>\S+)/$', views.votes, {'index': 'normal'}, name='votes'),
    url(r'^(?P<vote_id>\S+)/$', views.vote, name='vote'),
]
