from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout
from rest_framework import routers
from api import views


#--> rest framework url
router = routers.DefaultRouter()
router.register(r'councilors', views.CouncilorsViewSet)
router.register(r'councilors_terms', views.CouncilorsDetailViewSet)
router.register(r'sittings', views.SittingsViewSet)
router.register(r'votes', views.VotesViewSet)
router.register(r'councilors_votes', views.Councilors_VotesViewSet)
router.register(r'bills', views.BillsViewSet)
router.register(r'councilors_bills', views.Councilors_BillsViewSet)
router.register(r'attendance', views.AttendanceViewSet)
#<--

urlpatterns = patterns('',
    url(r'^councilors/', include('councilors.urls', namespace="councilors")),
    url(r'^bills/', include('bills.urls', namespace="bills")),
    url(r'^votes/', include('votes.urls', namespace="votes")),
    url(r'^about/$', 'voter_guide.views.about', name='about'),
    url(r'^reference/$', 'voter_guide.views.reference', name='reference'),
    url(r'', include('councilors.urls', namespace="councilors")),
    url(r'^api/', include(router.urls)),
)
