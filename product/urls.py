from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CartProductViewSet, ProductCategoryViewSet,
                    ProductDescriptionViewSet, ProductImageViewSet,
                    ProductSizeChartViewSet, ProductTagViewSet, ProductViewSet,
                    StoreViewSet, WishListProductViewSet, homepage_products,
                    search_products)

router = DefaultRouter()
router.register(r"category", ProductCategoryViewSet)
router.register(r"description", ProductDescriptionViewSet)
router.register(r"sizechart", ProductSizeChartViewSet)
router.register(r"product", ProductViewSet)
router.register(r"store", StoreViewSet)
router.register(r"image", ProductImageViewSet)
router.register(r"tag", ProductTagViewSet)
router.register(r"wishlist", WishListProductViewSet)
router.register(r"cart", CartProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('homepage-products/', homepage_products, name='homepage_products'),
    path('search/', search_products, name='search_products'),
]
