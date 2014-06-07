'''
Created on Apr 27, 2014

@author: carvey
'''
from django.conf.urls import patterns, url
from eagletrack import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        
)

