from django.conf.urls import url, include
from rest_framework import routers
from .views import ActiveViewSet


router = routers.DefaultRouter()
router.register(r'actives', ActiveViewSet)

actives_urls = [
	url(r'^api/', include(router.urls)),
]