'''
Created on Apr 27, 2014

@author: carvey
'''
from django.conf.urls import patterns, url
from personnel.views import Index, Stats, CadetListing, cadet_page, CompanyDetail, CompanyListing, \
    CompanyCadetListing, MSlevelListing, MScadetListing, MSLevelDetail, PlatoonDetail, Input, Login, logout, SquadDetail, \
    EditCompany, AddCompany, DeleteCompany

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

                        #TODO: All these needs converting to IDs instead of name
                       #Company/Platoon/Squad Pages
                       url(r'^companys/$', CompanyListing.as_view(), name='companylisting'),
                       url(r'^companys/(?P<company_id>\d+)/$', CompanyDetail.as_view(),
                           name='company_detail'),
                       url(r'^companys/(?P<company_id>\d+)/cadets$', CompanyCadetListing.as_view(),
                           name='cadets_in_company'),
                       url(r'^companys/(?P<company_id>\d+)/(?P<tab>\w+)/$', CompanyDetail.as_view(),
                           name='company_detail'),
                       url(r'^companys/(?P<company_id>\d+)/platoons/(?P<platoon_num>[-A-Za-z0-9_]+)/$',
                           PlatoonDetail.as_view(), name="platoon_detail"),
                       url(r'^companys/(?P<company_id>\d+)/platoons/(?P<platoon_num>[-A-Za-z0-9_]+)/squads/(?P<squad_num>[-A-Za-z0-9_]+)/$',
                           SquadDetail.as_view(), name="squad_detail"),
                       url(r'^companys/edit/(?P<company_id>\d+)/$', EditCompany.as_view(), name='edit_company'),
                       url(r'^companys/add/$', AddCompany.as_view(), name='add_company'),
                       url(r'^companys/delete/(?P<company_pk>\d+)/$', DeleteCompany.as_view(), name='delete_company'),

                       #MS Class Pages
                       url(r'^ms-classes/$', MSlevelListing.as_view(), name='mslisting'),
                       url(r'^ms-classes/(?P<ms_class>[-A-Za-z0-9_]+)/$', MSLevelDetail.as_view(), name='ms_detail'),
                       url(r'^ms-classes/(?P<ms_class>[-A-Za-z0-9_]+)/cadets/$', MScadetListing.as_view(),
                           name='mscadets'),
                       url(r'^ms-classes/(?P<ms_class>[-A-Za-z0-9_]+)/(?P<tab>\w+)/$', MSLevelDetail.as_view(),
                           name='ms_detail'),

                       #Dedicated input pages
                       url(r'^input/', Input.as_view(), name='input')
)