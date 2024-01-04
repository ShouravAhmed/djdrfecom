from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CartProductViewSet, ProductCategoryViewSet,
                    ProductDescriptionViewSet, ProductPhotoViewSet,
                    ProductSizeChartViewSet, ProductTagViewSet, ProductViewSet,
                    StoreViewSet, WishListProductViewSet)

router = DefaultRouter()
router.register(r"category", ProductCategoryViewSet)
router.register(r"description", ProductDescriptionViewSet)
router.register(r"sizechart", ProductSizeChartViewSet)
router.register(r"product", ProductViewSet)
router.register(r"store", StoreViewSet)
router.register(r"photo", ProductPhotoViewSet)
router.register(r"tag", ProductTagViewSet)
router.register(r"wishlist", WishListProductViewSet)
router.register(r"cart", CartProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
