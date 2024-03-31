import logging

from django.core.cache import cache

from common.services import (all_objects, delete_objects, filter_objects,
                             get_object)

from .models import (CartProduct, Product, ProductCategory, ProductDescription,
                     ProductImage, ProductSizeChart, ProductTag, Store,
                     WishListProduct)
from .serializers import (CartProductSerializer, ProductCategorySerializer,
                          ProductDescriptionSerializer, ProductImageSerializer,
                          ProductSerializer, ProductSizeChartSerializer,
                          ProductTagSerializer, StoreSerializer,
                          WishListProductSerializer)

logger = logging.getLogger('main')


class ProductCategoryCache:
    def __init__(self) -> None:
        self.__product_categories_cache_key = "PRODUCT_CATEGORIES_CACHE_KEY"

    def get_product_categories(self):
        if data := cache.get(self.__product_categories_cache_key):
            return data

        data = all_objects(ProductCategory.objects,
                           model_name="ProductCategory")
        sorted_data = sorted(data, key=lambda x: x.category_order)

        serializer = ProductCategorySerializer(sorted_data, many=True)
        cache.set(self.__product_categories_cache_key, serializer.data, 21600)

        return serializer.data

    def update_product_categories(self):
        data = all_objects(ProductCategory.objects,
                           model_name="ProductCategory")
        sorted_data = sorted(data, key=lambda x: x.category_order)

        serializer = ProductCategorySerializer(sorted_data, many=True)
        cache.set(self.__product_categories_cache_key, serializer.data, 21600)

        return serializer.data
