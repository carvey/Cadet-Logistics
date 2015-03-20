'''
Created on Apr 27, 2014

@author: carvey
'''
from django.conf.urls import patterns, url
from personnel.views import Index, Stats, CadetListing, cadet_page, CompanyDetail, company_listing, \
    CompanyCadetListing, MSlevelListing, MScadetListing, MSLevelDetail, PlatoonDetail, Input, Login, logout, SquadDetail, \
    EditCompany, AddCompany, DeleteCompany, GroupingDetail

urlpatterns = patterns('',
                       # site index
                       url(r'^$', Index.as_view(), name='index'),

                       #auth pages
                       url(r'^login/', Login.as_view(), name='login'),
                       url(r'^logout/', logout, name='logout'),

                       #General personnel stat page
                       url(r'^stats/$', Stats.as_view(), name='cadetstats'),
                       url(r'^stats/(?P<tab>\w+)/$', Stats.as_view(), name='cadetstats'),

                       #Cadet Page
                       url(r'^cadets/$', CadetListing.as_view(), name='cadetlisting'),
                       url(r'^cadets/(?P<cadet_id>[0-9]+)/$', cadet_page, name='cadetpage'),
                       url(r'^cadets/(?P<cadet_id>[0-9]+)/(?P<tab>\w+)/$', cadet_page, name='cadetpage'),

                       #Company/Platoon/Squad Pages

                       url(r'^(?P<grouping_type>[-A-Za-z_]+)/(?P<grouping_id>\d+)/$', GroupingDetail.as_view(), name="grouping_detail"),
                       url(r'^(?P<grouping_type>[-A-Za-z_]+)/(?P<grouping_id>\d+)/(?P<tab>\w+)/$', GroupingDetail.as_view(), name="grouping_detail"),

                       url(r'^companies/$', company_listing,
                           name='company_listing'),
                       # url(r'^companies/(?P<company_id>\d+)/$', CompanyDetail.as_view(),
                       #     name='company_detail'),
                       # url(r'^companies/(?P<company_id>\d+)/cadets$', CompanyCadetListing.as_view(),
                       #     name='cadets_in_company'),
                       # url(r'^companies/(?P<company_id>\d+)/(?P<tab>\w+)/$', CompanyDetail.as_view(),
                       #     name='company_detail'),
                       # url(r'^companies/(?P<company_id>\d+)/platoons/(?P<platoon_id>[-A-Za-z0-9_]+)/$',
                       #     PlatoonDetail.as_view(), name="platoon_detail"),
                       # url(r'^companies/(?P<company_id>\d+)/platoons/(?P<platoon_id>\d+)/squads/(?P<squad_id>\d+)/$',
                       #     SquadDetail.as_view(), name="squad_detail"),
                       url(r'^companies/edit/(?P<company_id>\d+)/$', EditCompany.as_view(), name='edit_company'),
                       url(r'^companies/add/$', AddCompany.as_view(), name='add_company'),
                       url(r'^companies/delete/(?P<company_id>\d+)/$', DeleteCompany.as_view(), name='delete_company'),

                       #MS Class Pages
                       url(r'^ms-classes/$', MSlevelListing.as_view(), name='mslisting'),
                       url(r'^ms-classes/(?P<ms_class_id>\d+)/$', MSLevelDetail.as_view(), name='ms_detail'),
                       url(r'^ms-classes/(?P<ms_class_id>\d+)/cadets/$', MScadetListing.as_view(),
                           name='mscadets'),
                       url(r'^ms-classes/(?P<ms_class_id>\d+)/(?P<tab>\w+)/$', MSLevelDetail.as_view(),
                           name='ms_detail'),

                       #Dedicated input pages
                       url(r'^input/', Input.as_view(), name='input')
)