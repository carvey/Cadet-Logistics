from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin

from personnel.views import Search, ReportProblem, Thanks, ProblemListing
from personnel.api.urls import urlpatterns as personnel_api
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', include('personnel.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^personnel/', include('personnel.urls')),
    url(r'^pt/', include('pt.urls')),
    url(r'^search/(?P<query_string>[-A-Za-z0-9_]+)/', Search.as_view(), name='search'),
    url(r'^report-a-problem/$', ReportProblem.as_view(), name='report'),
    url(r'^thanks/$', Thanks.as_view(), name='thanks'),
    url(r'^problems-listing/$', ProblemListing.as_view(), name='problems_listing'),

    url(r'^api/', include(personnel_api), name='api'),
)
if settings.DEBUG:
    urlpatterns += patterns (
        'django.views.static',
        (r'media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}), )