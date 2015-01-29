from django.conf.urls import patterns, url
from pt.views import *

urlpatterns = patterns('',
        
        url(r'^tests/scores/(?P<test_id>\d+)/?$', TestScoresView.as_view(), name='scores-by-test'),
        
        url(r'^tests/?$', TestListingView.as_view(), name='pt-tests-index'),
        url(r'^tests/(?P<test_id>\d+)/$', TestProfiletView.as_view(), name='pt-test-profile'),
        url(r'^tests/(?P<test_id>\d+)/(?P<tab>\w+)/$', TestProfiletView.as_view(), name='pt-test-profile'),
        
        url(r'^cadet/(?P<cadet_id>\d+)/?$', CadetDetailView.as_view(), name='cadet-detail-view'),
        
        url(r'^stats/?$', StatisticsView.as_view(), name='pt-stats'),

        url(r'^stats/(?P<tab>\s+)/?$', StatisticsView.as_view(), name='pt-stats-tab'),

        url(r'^cadets/listing/?$', CadetsListingView.as_view(), name='pt-cadets-listing'),
        
        url(r'^cadets', CadetsListingView.as_view(), name='pt-cadets-listing'),

    )