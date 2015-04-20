from django.conf.urls import patterns, url
from pt.views import *

urlpatterns = patterns('',

        url(r'^input/', PTInfo.as_view(), name='pt-input'),
        
        url(r'^tests/scores/(?P<test_id>\d+)/?$', TestScoresView.as_view(), name='scores-by-test'),
        
        url(r'^tests/?$', TestListingView.as_view(), name='pt-tests-listing'),
        url(r'^tests/add', AddTest.as_view(), name='add_pt_test'),
        url(r'^tests/edit/(?P<test_id>\d+)/$', EditTest.as_view(), name='edit_pt_test'),

        url(r'^tests/input-scores/(?P<test_id>\d+)/$', InputTestScores.as_view(), name='input_test_scores'),
        url(r'^tests/input-scores/(?P<cadet_id>\d+)/(?P<situps>\d+)/(?P<pushups>\d+)/(?P<two_mile>[0-5]?[0-9]:[0-5]?[0-9])/$', calculate_score, name='calculate-score'),

        url(r'^tests/input-scores/(?P<gender>\w+)/(?P<age>\w+)/(?P<situps>\d+)/(?P<pushups>\d+)/(?P<two_mile>[0-5]?[0-9]:[0-5]?[0-9])/$', calculate_score),

        url(r'^tests/(?P<test_id>\d+)/$', TestProfiletView.as_view(), name='pt-test-profile'),
        url(r'^tests/(?P<test_id>\d+)/(?P<tab>\w+)/$', TestProfiletView.as_view(), name='pt-test-profile'),
        
        url(r'^stats/?$', StatisticsView.as_view(), name='pt-stats'),

        url(r'^stats/(?P<tab>\s+)/?$', StatisticsView.as_view(), name='pt-stats-tab'),
        
        url(r'^cadets', CadetsListingView.as_view(), name='pt-cadets-listing'),

        url(r'^calculator', PTCalculator.as_view(), name='calculator')

    )