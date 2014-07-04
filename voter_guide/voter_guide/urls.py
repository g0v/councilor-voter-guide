from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^councilors/', include('councilors.urls', namespace="councilors")),
    url(r'^bills/', include('bills.urls', namespace="bills")),
    url(r'^about/$', 'voter_guide.views.about', name='about'),
    url(r'^reference/$', 'voter_guide.views.reference', name='reference'),
    url(r'', include('councilors.urls', namespace="councilors")),
#   url(r'', include('social_auth.urls')),
#   url(r'^accounts/login/$', login, name='login'),
#   url(r'^accounts/logout/$', 'voter_guide.views.logout', name='logout'),
)
