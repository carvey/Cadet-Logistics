'''
Created on Apr 27, 2014

@author: carvey
'''
from django.conf.urls import patterns, url
from eagletrack.views import index, CPview, Dashboard, CadetStats, CompanyStats, MSlevelStats

urlpatterns = patterns('',
        url(r'^$', index, name='index'),
        url(r'^cp', CPview.as_view(), name='cpview'),
        url(r'^dash', Dashboard.as_view(), name='dashboard'),
        url(r'^cadet', CadetStats.as_view(), name='cadetstats'),
        url(r'^company', CompanyStats.as_view(), name='sompanystats'),
        url(r'ms', MSlevelStats.as_view(), name='msstats'),
        
)

