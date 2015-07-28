'''
Created on Apr 27, 2014

@author: carvey
'''
from django.conf.urls import patterns, url
from personnel.views import Index, Stats, CadetListing, cadet_page, company_listing, \
    CompanyCadetListing, MSlevelListing, MScadetListing, Input, Login, logout, \
    EditCompany, AddCompany, DeleteCompany, GroupingDetail, CadetRegistration, \
    organize, CadreRegistration, save_organization_change_records

urlpatterns = patterns('',
                       # site index
                       url(r'^$', Index.as_view(), name='index'),

                       #auth pages
                       url(r'^login/', Login.as_view(), name='login'),
                       url(r'^logout/', logout, name='logout'),

                       #General personnel stat page
                       url(r'^stats/$', Stats.as_view(), name='cadetstats'),
                       url(r'^stats/(?P<tab>\w+)/$', Stats.as_view(), name='cadetstats'),

                       #Cadre
                       url(r'cadre/register', CadreRegistration.as_view(), name='cadre_registration'),

                       #Cadet Page
                       url(r'^cadets/$', CadetListing.as_view(), name='cadetlisting'),
                       url(r'^cadets/register', CadetRegistration.as_view(), name='cadet_registration'),
                       url(r'^cadets/(?P<cadet_id>[0-9]+)/$', cadet_page, name='cadetpage'),
                       url(r'^cadets/(?P<cadet_id>[0-9]+)/(?P<tab>\w+)/$', cadet_page, name='cadetpage'),

                       #Company/Platoon/Squad Pages

                       url(r'^(?P<grouping_type>[-A-Za-z_]+)/(?P<grouping_id>\d+)/$', GroupingDetail.as_view(), name="grouping_detail"),
                       url(r'^(?P<grouping_type>[-A-Za-z_]+)/(?P<grouping_id>\d+)/(?P<tab>\w+)/$', GroupingDetail.as_view(), name="grouping_detail"),

                       url(r'^companies/$', company_listing,
                           name='company_listing'),
                       url(r'^companies/edit/(?P<company_id>\d+)/$', EditCompany.as_view(), name='edit_company'),
                       url(r'^companies/add/$', AddCompany.as_view(), name='add_company'),
                       url(r'^companies/delete/(?P<company_id>\d+)/$', DeleteCompany.as_view(), name='delete_company'),

                       #MS Class Pages
                       url(r'^ms-classes/$', MSlevelListing.as_view(), name='mslisting'),
                       url(r'^ms-classes/(?P<ms_class_id>\d+)/cadets/$', MScadetListing.as_view(),
                           name='mscadets'),

                       #Dedicated input pages
                       url(r'^input/', Input.as_view(), name='input'),

                       url(r'^organize/$', organize, name="organize_staff"),
                       url(r'^organize/save/$', save_organization_change_records, name="organize_staff_save"),
)