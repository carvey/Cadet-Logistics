'''
Created on Apr 27, 2014

@author: carvey
'''
from django.conf.urls import patterns, url
from eagletrack.views import index, CPview, Dashboard, CadetStats, CadetListing, CompanyStats, CompanyListing, MSlevelStats, MSlevelListing

urlpatterns = patterns('',
        url(r'^$', index.as_view(), name='index'),
        url(r'^cp', CPview.as_view(), name='cpview'),
        url(r'^dash', Dashboard.as_view(), name='dashboard'),
        url(r'^cadetstats', CadetStats.as_view(), name='cadetstats'),
        url(r'^cadetlisting', CadetListing.as_view(), name='cadetlisting'),
        url(r'^companystats', CompanyStats.as_view(), name='companystats'),
        url(r'^companylisting', CompanyListing.as_view(), name='companylisting'),
        url(r'^msstats$', MSlevelStats.as_view(), name='msstats'),
        url(r'^mslisting', MSlevelListing.as_view(), name='mslisting'),
        
)

