import datetime

from django.contrib.auth import authenticate
from django.db import transaction
from django.shortcuts import render
from django.utils.translation import gettext as _
from django_ratelimit.decorators import ratelimit
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, serializers, status, viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response

from common.services import (all_objects, delete_objects, filter_objects,
                             get_object)

from .enums import DiscountType, OfferType
from .models import Banner, Offer
from .serializers import BannerSerializer
from .utils import BannerCache


class BannerViewSet(viewsets.ViewSet):
    """
    Viewset for Banner
    """
    cache_provider = BannerCache()
    queryset = all_objects(Banner.objects,
                           model_name="Banner")

    def __fix_banner_order(self):
        banners = all_objects(
            Banner.objects, model_name="Banner")
        sorted_banners = sorted(banners, key=lambda x: x.banner_order)

        with transaction.atomic():
            for order, banner in enumerate(sorted_banners, start=1):
                banner.banner_order = order
                banner.save()

    def __update_banner_order(self, order):
        banners = all_objects(
            Banner.objects, model_name="Banner")

        with transaction.atomic():
            for banner in banners:
                banner.banner_order = order[banner.title]
                banner.save()

    @extend_schema(responses=BannerSerializer(many=True))
    def list(self, request):
        """Return all banners."""
        return Response(self.cache_provider.get_banners(), status=status.HTTP_200_OK)

    @extend_schema(responses=BannerSerializer)
    @permission_classes([permissions.IsAuthenticated, permissions.IsAdminUser])
    def create(self, request):
        """An endpoint to create or update a banner"""
        if not authenticate(username=request.user.username, password=request.data.get('admin_password', '')):
            return Response({'message': 'Admin Password Required'}, status=status.HTTP_401_UNAUTHORIZED)

        request_data = request.data.copy()

        if isinstance(request_data.get('image', ''), str):
            del request_data['image']

        banner_title = request_data.get('previous_title', None)
        banner = filter_objects(
            Banner.objects,
            fields={
                'title': banner_title,
            },
            model_name='Banner'
        ) if banner_title else None

        if banner:
            instance = banner[0]
            serializer = BannerSerializer(instance, data=request_data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_204_NO_CONTENT)
        else:
            request_data['banner_order'] = 1000

            serializer = BannerSerializer(data=request_data)
            if serializer.is_valid():
                serializer.save()
                self.__fix_banner_order()
            else:
                return Response(serializer.errors, status=status.HTTP_204_NO_CONTENT)
        return Response(self.cache_provider.update_banners(), status=status.HTTP_200_OK)

    @extend_schema(responses=BannerSerializer)
    @permission_classes([permissions.IsAuthenticated, permissions.IsAdminUser])
    @action(detail=False, methods=['post'], url_path="delete", url_name="delete_banner")
    def delete_banner(self, request):
        """Delete a banner."""
        if not authenticate(username=request.user.username, password=request.data.get('admin_password', '')):
            return Response({'message': 'Admin Password Required'}, status=status.HTTP_401_UNAUTHORIZED)

        instance = get_object(
            Banner.objects,
            fields={'title': request.data.get('title'), },
            model_name="Banner"
        )
        instance.delete()
        self.__fix_banner_order()
        return Response(self.cache_provider.update_banners(), status=status.HTTP_200_OK)

    @extend_schema(responses=BannerSerializer)
    @permission_classes([permissions.IsAuthenticated, permissions.IsAdminUser])
    @action(detail=False, methods=['post'], url_path="update-order", url_name="update_banner_order")
    def update_banner_order(self, request):
        """Update the order of product categories."""
        self.__update_banner_order(request.data.get('order'))
        return Response(self.cache_provider.update_banners(), status=status.HTTP_200_OK)


class OfferViewSet(viewsets.ViewSet):
    """
    Viewset for Offer
    """
    queryset = all_objects(Offer.objects,
                           model_name="Offer")

    @action(
        detail=False,
        methods=['get'],
        url_path=r"validate-coupon/(?P<coupon>[^/]+)",
        url_name="validate-coupon"
    )
    def validate_coupon(self, request, coupon):
        """
        Validate if given `string` is a valid coupon and 
        return a response with key `is_valid` (Boolean), 
        `discount_type` (Enum: 'PERCENTAGE', 'FIXED') and `discount_value` (Integer).
        """
        ip = request.META['REMOTE_ADDR']

        today = datetime.date.today()

        offers = filter_objects(
            Offer.objects,
            fields={
                'duration_day__gte': today,
                'offer_type': OfferType.PROMO_CODE,
            },
            model_name='Offer'
        )

        for offer in offers:
            if offer.promo_code == coupon:
                res = {'is_valid': True, }
                if offer.discount_type == DiscountType.PERCENTAGE:
                    res['discount_type'] = 'PERCENTAGE'
                else:
                    res['discount_type'] = 'FIXED'
                res['discount_value'] = offer.discount_value
                return Response(res, status=status.HTTP_200_OK)

        return Response({'is_valid': False}, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=['get'],
        url_path="flat-discount",
        url_name="flat-discount"
    )
    def flat_discount(self, request):
        """
        Check if there is a flat discount available and 
        return a response with key `is_available` (Boolean), 
        `discount_type` (Enum: 'PERCENTAGE', 'FIXED') and `discount_value` (Integer).
        """
        today = datetime.date.today()

        offers = filter_objects(
            Offer.objects,
            fields={
                'duration_day__gte': today,
                'offer_type': OfferType.FLAT_DISCOUNT,
            },
            model_name='Offer'
        )

        if len(offers) > 0:
            offer = offers[0]
            res = {'is_available': True, }
            if offer.discount_type == DiscountType.PERCENTAGE:
                res['discount_type'] = 'PERCENTAGE'
            else:
                res['discount_type'] = 'FIXED'
            res['discount_value'] = offer.discount_value
            return Response(res, status=status.HTTP_200_OK)

        return Response({'is_available': False}, status=status.HTTP_200_OK)
