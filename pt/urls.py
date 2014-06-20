from django.conf.urls import patterns, url
from pt.views import Dashboard, CpView, TestView, CadetsView, CompanyView, MsLevelView

urlpatterns = patterns('',
        url(r'^$', Dashboard.as_view()),
        url(r'^cp', CpView.as_view()),
        url(r'^tests', TestView.as_view()),
        url(r'^cadets', CadetsView.as_view()),
        url(r'^company', CompanyView.as_view()),
        url(r'^mslevel', MsLevelView.as_view()),        
    )