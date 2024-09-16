from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import OrderedProductViewSet, OrderViewSet

router = DefaultRouter()
router.register(r"", OrderViewSet)
router.register(r"ordered-product", OrderedProductViewSet)
urlpatterns = [
    path('', include(router.urls)),
]
