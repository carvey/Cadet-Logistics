'''
Created on Apr 27, 2014

@author: carvey
'''
from django.conf.urls import patterns, url
from personnel.views import index, CPview, Dashboard, CadetStats, CadetListing, CadetPage, CompanyStats, CompanyListing, CompanyCadetListing, MSlevelStats, MSlevelListing, MScadetListing

urlpatterns = patterns('',
        url(r'^$', index.as_view(), name='index'),
        url(r'^cp', CPview.as_view(), name='cpview'),
        url(r'^dash', Dashboard.as_view(), name='dashboard'),
        
        url(r'^cadetstats', CadetStats.as_view(), name='cadetstats'),
        url(r'^cadetlisting', CadetListing.as_view(), name='cadetlisting'),
        url(r'^cadets/(?P<cadet_id>[0-9]+)/$', CadetPage.as_view(), name='cadetpage'),
        
        url(r'^companystats', CompanyStats.as_view(), name='companystats'),
        url(r'^companylisting', CompanyListing.as_view(), name='companylisting'),
        url(r'^companycadets/(?P<company_name>[-A-Za-z0-9_]+)/$', CompanyCadetListing.as_view(), name='cadets_in_company'),
        
        url(r'^msstats$', MSlevelStats.as_view(), name='msstats'),
        url(r'^mslisting', MSlevelListing.as_view(), name='mslisting'),
        url(r'^mscadets/(?P<ms_class>[-A-Za-z0-9_]+)/$', MScadetListing.as_view(), name='mscadets'),
        
)

