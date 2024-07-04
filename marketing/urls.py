from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import BannerViewSet, OfferViewSet

router = DefaultRouter()
router.register(r"banner", BannerViewSet)
router.register(r"offer", OfferViewSet)
urlpatterns = [
    path('', include(router.urls)),
]
