from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ProductCategoryViewSet

router = DefaultRouter()
router.register(r"", ProductCategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
