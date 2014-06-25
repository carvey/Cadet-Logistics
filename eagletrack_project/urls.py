from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', include('personnel.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^personnel/', include('personnel.urls')),
    url(r'^pt/', include('pt.urls')),
)
if settings.DEBUG:
    urlpatterns += patterns (
        'django.views.static',
        (r'media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}), )