import datetime
import logging

from django.core.cache import cache

from common.services import (all_objects, delete_objects, filter_objects,
                             get_object)

from .enums import DiscountType, OfferType
from .models import Banner, Offer
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


def cached_coupon(coupon):
    if data := cache.get(f"CACHED_COUPON_CODE_{coupon}"):
        logger.info(f"Cashed Coupon: {data}\n\n")
        return data

    today = datetime.date.today()
    offers = filter_objects(
        Offer.objects,
        fields={
            'duration_day__gte': today,
            'offer_type': OfferType.PROMO_CODE,
            'promo_code': coupon
        },
        model_name='Offer'
    )

    res = {'is_valid': False, }
    if len(offers) > 0:
        offer = offers[0]
        res['is_valid'] = True
        if offer.discount_type == DiscountType.PERCENTAGE:
            res['discount_type'] = 'PERCENTAGE'
        else:
            res['discount_type'] = 'FIXED'
        res['discount_value'] = offer.discount_value
        res['promo_code'] = str(coupon)

    cache.set(f"CACHED_COUPON_CODE_{coupon}", res, 3600)

    logger.info(f"DB Coupon: {res}\n\n")
    return res


def cached_flat_discount():
    if data := cache.get("CACHED_FLAT_DISCOUNT"):
        logger.info(f"CACHED_FLAT_DISCOUNT: {data}\n\n")
        return data

    today = datetime.date.today()
    offers = filter_objects(
        Offer.objects,
        fields={
            'duration_day__gte': today,
            'offer_type': OfferType.FLAT_DISCOUNT,
        },
        model_name='Offer'
    )

    res = {'is_available': False, }
    if len(offers) > 0:
        offer = offers[0]
        res['is_available'] = True
        if offer.discount_type == DiscountType.PERCENTAGE:
            res['discount_type'] = 'PERCENTAGE'
        else:
            res['discount_type'] = 'FIXED'
        res['discount_value'] = offer.discount_value

    cache.set("CACHED_FLAT_DISCOUNT", res, 3600)

    logger.info(f"DB_FLAT_DISCOUNT: {res}\n\n")
    return res
