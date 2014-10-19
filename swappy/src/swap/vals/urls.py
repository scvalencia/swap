from django.conf.urls import url, include
from rest_framework import routers
from .views import RentViewSet, ValViewSet


router = routers.DefaultRouter()
router.register(r'rents', RentViewSet)
router.register(r'vals', ValViewSet)

vals_urls = [
	url(r'^api/', include(router.urls)),
]