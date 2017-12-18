from django.conf.urls import include, url
from django.conf import settings

from rest_framework import routers

from api import views
from . import views as voter_guide_views
from candidates import views as candidates_views


#--> rest framework url
router = routers.DefaultRouter()
router.register(r'candidates', views.CandidatesViewSet)
router.register(r'councilors', views.CouncilorsViewSet)
router.register(r'councilors_terms', views.CouncilorsDetailViewSet)
router.register(r'sittings', views.SittingsViewSet)
router.register(r'votes', views.VotesViewSet)
router.register(r'councilors_votes', views.Councilors_VotesViewSet)
router.register(r'bills', views.BillsViewSet)
router.register(r'councilors_bills', views.Councilors_BillsViewSet)
router.register(r'attendance', views.AttendanceViewSet)
router.register(r'suggestions', views.SuggestionsViewSet)
router.register(r'councilors_suggestions', views.Councilors_SuggestionsViewSet)
#<--

urlpatterns = [
    url(r'^accounts/', include('allauth.urls')),
    url(r'^candidates/', include('candidates.urls', namespace="candidates")),
    url(r'^platforms/', include('platforms.urls', namespace="platforms")),
    url(r'^councilors/', include('councilors.urls', namespace="councilors")),
    url(r'^suggestions/', include('suggestions.urls', namespace="suggestions")),
    url(r'^bills/', include('bills.urls', namespace="bills")),
    url(r'^votes/', include('votes.urls', namespace="votes")),
    url(r'^users/', include('users.urls', namespace="users")),
    url(r'^dispatch/$', voter_guide_views.dispatch, name='dispatch'),
    url(r'^about/$', voter_guide_views.about, name='about'),
    url(r'^select_county/(?P<category>candidates|councilors|bills|votes)/$', voter_guide_views.select_county, name='select_county'),
    url(r'^reference/$', voter_guide_views.reference, name='reference'),
    url(r'^$', voter_guide_views.select_county, {'category': 'candidates'}, name='select_county'),
    url(r'^api/', include(router.urls)),
    url(r'^api/check_person_name/$', views.check_person_name),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
