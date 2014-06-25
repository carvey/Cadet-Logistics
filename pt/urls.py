from django.conf.urls import patterns, url
from pt.views import *

urlpatterns = patterns('',
        url(r'^$', Dashboard.as_view(), name='pt-index'),
        
        url(r'^dash/?$', Dashboard.as_view(), name='pt-dashboard'),
        
        url(r'^cp', CpView.as_view(), name='pt-cp'),
        
        url(r'^tests/stats/?$', TestStatView.as_view(), name='pt-tests-stats'),
        
        url(r'^tests/listing/?$', TestListingView.as_view(), name='pt-tests-listing'),
        
        url(r'^tests/?$', TestView.as_view(), name='pt-tests-index'),
        
        url(r'^cadet/(?P<cadet_id>\d+)/?$', CadetDetailView.as_view(), name='cadet-detail-view'),
        
        url(r'^cadets/stats/?$', CadetsStatView.as_view(), name='pt-cadets-stats'),
        
        url(r'^cadets/listing/?$', CadetsListingView.as_view(), name='pt-cadets-listing'),
        
        url(r'^cadets', CadetsView.as_view(), name='pt-cadets-listing'),
        
        url(r'^company/stats/?$', CompanyStatView.as_view(), name='pt-compnay-stats'),
        
        url(r'^company/listing/?$', CompanyListingView.as_view(), name='pt-company-listing'),
        
        url(r'^company', CompanyView.as_view(), name='pt-company-index'),
        
        url(r'^ms/stats/?$', MsLevelStatView.as_view(), name='pt-ms-stats'),
        
        url(r'^ms/listing/?$', MsLevelListingView.as_view(), name='pt-ms-stats'),
        
        url(r'^ms', MsLevelView.as_view(), name='pt-ms-index'),        
    )