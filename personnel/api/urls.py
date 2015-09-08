from django.conf.urls import patterns, include, url
from endpoints import CadetEndPoint

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'cadets', CadetEndPoint)

urlpatterns = [
    url(r'^', include(router.urls)),
]