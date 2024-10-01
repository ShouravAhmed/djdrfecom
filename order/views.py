import datetime
import logging

from django.contrib.auth import authenticate
from django.db import transaction
from django.db.models import Q
from django.shortcuts import render
from django.utils.translation import gettext as _
from django_ratelimit.decorators import ratelimit
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, serializers, status, viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response

from authentication.models import User
from common.services import (all_objects, delete_objects, filter_objects,
                             get_object)
from common.utils import is_vaid_phone_number
from marketing.utils import cached_coupon, cached_flat_discount
from product.models import CartProduct, Product, ProductStock

from .enums import ReviewStatus
from .models import Order, OrderedProduct
from .serializers import OrderedProductSerializer, OrderSerializer

logger = logging.getLogger('main')


class OrderViewSet(viewsets.ViewSet):
    """
    Viewset for Order
    """
    queryset = all_objects(Order.objects, model_name="Order")

    @extend_schema(responses=OrderSerializer)
    @permission_classes([permissions.IsAuthenticated])
    def list(self, request):
        """
        An endpoint to retrieve a user's orders
        """
        user_orders = filter_objects(
            Order.objects,
            fields={
                'customer': request.user,
            },
            model_name='Order'
        ).order_by('-created_at')

        serializer = OrderSerializer(
            user_orders,
            context={'request': request},
            many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(responses=OrderSerializer)
    @permission_classes([permissions.IsAuthenticated])
    @action(
        methods=['get'],
        detail=False,
        url_path=r"(?P<order_id>[^/]+)",
        url_name="order_by_id"
    )
    def order_by_id(self, request, order_id=None):
        """
        An endpoint to return single order by `order_id`
        """
        serializer = OrderSerializer(
            get_object(
                all_objects(Order.objects.prefetch_related(
                    'orderedproduct_set', 'ordernote_set'), model_name="Order"),
                fields={
                    'order_id': order_id,
                },
                model_name='Order'
            ),
            context={'request': request},
            many=False
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(responses=OrderSerializer)
    @action(
        methods=['post'],
        detail=False,
        url_path="confirm",
        url_name="confirm_order"
    )
    def confirm_order(self, request):
        """
        An endpoint to create a order
        """
        try:
            cart_item_list = request.data.get('cart_item_list', [])
            logger.info(f"cart_item_list: {cart_item_list}\n")

            delivery_details = request.data.get('delivery_details', {})
            logger.info(f"delivery_details: {delivery_details}\n")

            applied_coupon = request.data.get('applied_coupon', {})
            logger.info(f"applied_coupon: {applied_coupon}\n")

            if not is_vaid_phone_number(delivery_details.get('phone', '')):
                return Response({'status': 'FAILED', 'message': 'Phone no is not correct.'}, status=status.HTTP_200_OK)

            user = request.user
            anonymous_user = False

            if user.is_anonymous:
                anonymous_user = True
                user, created = User.objects.get_or_create(
                    phone_number=delivery_details.get('phone'))

            logger.info(f"User is {user}\n")

            created_order = Order.objects.create(
                customer=user,
                customer_name=delivery_details.get('name', ''),
                customer_phone=delivery_details.get('phone'),
                customer_email=delivery_details.get('email', ''),
                customer_address=f"{delivery_details.get('address', '')}, {delivery_details.get('district', '')}",
                customer_note=delivery_details.get('note', ''),
            )

            products_base_value = 0
            products_regular_value = 0
            products_discount = 0
            flat_discount = 0
            additional_discount = 0
            customers_delivery_charge = 0
            amount_to_collect = 0

            for item in cart_item_list:
                try:
                    product = get_object(
                        Product.objects,
                        fields={
                            'product_id': item['product']['product_id'],
                        },
                        model_name='Product'
                    )
                    stock = ProductStock.objects.filter(
                        product=product, size=item['size']).first()
                    product_quantity = min(
                        stock.count if stock else 0, int(item['count']))

                    if product_quantity <= 0:
                        continue

                    stock.count = stock.count - product_quantity
                    stock.save()

                    ordered_product = OrderedProduct.objects.create(
                        order=created_order,
                        product=product,
                        product_size=item['size'],
                        product_price=(
                            float(product.product_selling_price) - ((float(product.product_selling_price) *
                                                                     float(product.product_discount)) / 100.0)
                        ),
                        product_quantity=product_quantity
                    )

                    products_base_value += (
                        int(product.product_base_price) * product_quantity
                    )
                    products_regular_value += (
                        int(product.product_selling_price) * product_quantity
                    )
                    products_discount += (
                        ((int(product.product_selling_price) *
                          int(product.product_discount)) / 100.0) * product_quantity
                    )

                except Exception as e:
                    logger.error(f"OrderedProduct creating Exception: {e}\n")

            if not anonymous_user:
                try:
                    cart_items = filter_objects(
                        CartProduct.objects,
                        fields={
                            'user': user,
                        },
                        model_name='CartProduct'
                    )
                    for item in cart_items:
                        item.delete()
                except Exception as e:
                    logger.error(f"Cart item deleting Exception: {e}\n")

            if applied_coupon:
                try:
                    coupon = cached_coupon(
                        applied_coupon.get('promo_code', ''))
                    if coupon['is_valid']:
                        if coupon['discount_type'] == 'FIXED':
                            flat_discount = int(coupon['discount_value'])
                        else:
                            flat_discount = (
                                (products_regular_value - products_discount) *
                                int(coupon['discount_value'])
                            ) / 100.0
                except Exception as e:
                    logger.error(f"coupon discount Exception: {e}\n")

            if flat_discount <= 0:
                try:
                    discount = cached_flat_discount()
                    if discount['is_available']:
                        if discount['discount_type'] == 'FIXED':
                            flat_discount = int(discount['discount_value'])
                        else:
                            flat_discount = (
                                ((products_regular_value - products_discount) * int(discount['discount_value'])) / 100.0)
                except Exception as e:
                    logger.error(f"Flat discount Exception: {e}\n")

            order_subtotal = float(
                (products_regular_value - products_discount) - flat_discount
            )

            if order_subtotal >= 999:
                customers_delivery_charge = 0
            else:
                if delivery_details.get('district', '') == 'Dhaka':
                    customers_delivery_charge = 60
                else:
                    customers_delivery_charge = 120

            order_subtotal += customers_delivery_charge

            rounding_discount = order_subtotal - \
                (int(order_subtotal / 10) * 10)

            if order_subtotal >= 999:
                additional_discount = int((order_subtotal-1000+1)/1000) * 100
            additional_discount += rounding_discount

            amount_to_collect = int(order_subtotal - additional_discount)

            logger.info(f"products_base_value : {products_base_value}")
            logger.info(f"products_regular_value : {products_regular_value}")
            logger.info(f"products_discount : {products_discount}")
            logger.info(f"flat_discount : {flat_discount}")
            logger.info(f"order_subtotal : {order_subtotal}")
            logger.info(f"additional_discount : {additional_discount}")
            logger.info(
                f"customers_delivery_charge: {customers_delivery_charge}")
            logger.info(f"amount_to_collect: {amount_to_collect}")

            created_order.products_base_value = products_base_value
            created_order.products_regular_value = products_regular_value
            created_order.products_discount = products_discount
            created_order.flat_discount = flat_discount
            created_order.additional_discount = additional_discount
            created_order.customers_delivery_charge = customers_delivery_charge
            created_order.amount_to_collect = amount_to_collect
            created_order.save()

            serializer = OrderSerializer(
                created_order,
                context={'request': request},
                many=False
            )
            return Response({'status': 'OK', 'data': serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Conform Order Exception: {e}\n")
            return Response({'status': 'FAILED', }, status=status.HTTP_200_OK)


class OrderedProductViewSet(viewsets.ViewSet):
    """
    Viewset for OrderedProducts
    """
    queryset = all_objects(OrderedProduct.objects, model_name="OrderedProduct")

    @extend_schema(responses=OrderedProductSerializer)
    @permission_classes([permissions.IsAuthenticated])
    @action(
        methods=['post'],
        detail=False,
        url_path="review",
        url_name="update_review"
    )
    def update_review(self, request):
        """
        An endpoint to update a review
        """
        try:
            data = request.data.get('review', {})
            product = get_object(
                Product.objects,
                fields={
                    'product_id': data['product']['product_id'],
                },
                model_name='Product'
            )
            order = get_object(
                Order.objects,
                fields={
                    'order_id': data['order']['order_id'],
                },
                model_name='Order'
            )
            ordered_product = OrderedProduct.objects.get(
                product=product,
                order=order,
                product_size=data['size'],
            )
            if ordered_product.review_status == ReviewStatus.APPROVED:
                return Response({'status': 'FAILED'}, status=status.HTTP_200_OK)

            ordered_product.rating = float(data['rating'])
            ordered_product.review = data['description']
            ordered_product.review_status = ReviewStatus.SUBMITTED
            ordered_product.save()

            return Response({'status': 'OK'}, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"exception: {e}")
            return Response({'status': 'FAILED', }, status=status.HTTP_200_OK)

    @extend_schema(responses=OrderedProductSerializer)
    @action(
        methods=['get'],
        detail=False,
        url_path=r"review/(?P<product_id>[^/]+)",
        url_name="product_review_list"
    )
    def product_review_list(self, request, product_id=None):
        """
        An endpoint to return products reviews by product
        """
        user = request.user
        reviews = filter_objects(
            all_objects(OrderedProduct.objects, model_name="OrderedProduct"),
            fields={
                'product__product_id': product_id,
            },
            model_name='OrderedProduct'
        )

        if user and not user.is_staff:
            reviews = reviews.filter(
                Q(review_status=ReviewStatus.APPROVED) | Q(order__customer=user)
            )

        reviews = reviews.order_by('-rating')

        serializer = OrderedProductSerializer(
            reviews,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)
