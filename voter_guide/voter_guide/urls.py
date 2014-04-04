from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'voter_guide.views.home', name='home'),
    # url(r'^voter_guide/', include('voter_guide.foo.urls')),
    url(r'', include('social_auth.urls')),
    url(r'^accounts/login/$', login, name='login'),
    url(r'^accounts/logout/$', 'voter_guide.views.logout', name='logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
