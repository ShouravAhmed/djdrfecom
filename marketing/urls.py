from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import BannerViewSet

router = DefaultRouter()
router.register(r"banner", BannerViewSet)
urlpatterns = [
    path('', include(router.urls)),
]
