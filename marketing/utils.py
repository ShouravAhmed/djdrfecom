import logging

from django.core.cache import cache

from common.services import (all_objects, delete_objects, filter_objects,
                             get_object)

from .models import Banner
from .serializers import BannerSerializer

logger = logging.getLogger('main')


class BannerCache:
    def __init__(self) -> None:
        self.__banner_cache_key = "BANNER_CACHE_KEY"

    def get_banners(self):
        if data := cache.get(self.__banner_cache_key):
            return data
        data = all_objects(Banner.objects,
                           model_name="Banner")
        sorted_data = sorted(data, key=lambda x: x.banner_order)

        serializer = BannerSerializer(sorted_data, many=True)
        cache.set(self.__banner_cache_key, serializer.data, 21600)

        return serializer.data

    def update_banners(self):
        data = all_objects(Banner.objects,
                           model_name="Banner")
        sorted_data = sorted(data, key=lambda x: x.banner_order)

        serializer = BannerSerializer(sorted_data, many=True)
        cache.set(self.__banner_cache_key, serializer.data, 21600)

        return serializer.data
