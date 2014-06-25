from django.conf.urls import patterns, url
from pt.views import *

urlpatterns = patterns('',
        url(r'^$', Dashboard.as_view()),
        
        url(r'^dash/?$', Dashboard.as_view()),
        
        url(r'^cp', CpView.as_view()),
        
        url(r'^tests/stats/?$', TestStatView.as_view()),
        
        url(r'^tests/listing/?$', TestListingView.as_view()),
        
        url(r'^tests/?$', TestView.as_view()),
        
        url(r'^cadets/stats/?$', CadetsStatView.as_view()),
        
        url(r'^cadets/listing/?$', CadetsListingView.as_view()),
        
        url(r'^cadets', CadetsView.as_view()),
        
        url(r'^company', CompanyView.as_view()),
        
        url(r'^mslevel', MsLevelView.as_view()),        
    )