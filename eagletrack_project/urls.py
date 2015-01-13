from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin

from personnel.views import Login, logout
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', include('personnel.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^personnel/', include('personnel.urls')),
    url(r'^pt/', include('pt.urls')),
    url(r'^login/', Login.as_view(), name='login'),
    url(r'^logout/', logout, name='logout')
)
if settings.DEBUG:
    urlpatterns += patterns (
        'django.views.static',
        (r'media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}), )