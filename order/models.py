import datetime
import logging
import random
import string

from django.apps import apps
from django.db import models

from authentication.models import User
from common.pathao import PathaoApi
from product.models import Product, Store

from .enums import (CourierOption, DeliveryType, ItemType, OrderStatus,
                    PaymentMethod, PaymentStatus)

logger = logging.getLogger('main')


class City(models.Model):
    courier_choice = models.IntegerField(choices=CourierOption.choices)
    city_id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=50)

    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['courier_choice']),
        ]


class Zone(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    zone_id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=100)

    class Meta:
        indexes = [
            models.Index(fields=['city']),
            models.Index(fields=['name']),
        ]


class Area(models.Model):
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE)
    area_id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=150)
    home_delivery_available = models.BooleanField()
    pickup_available = models.BooleanField()

    class Meta:
        unique_together = ['area_id', 'name']

    class Meta:
        indexes = [
            models.Index(fields=['zone']),
            models.Index(fields=['name']),
        ]


class CourierStore(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    courier_choice = models.IntegerField(choices=CourierOption.choices)
    courier_store_id = models.IntegerField(primary_key=True, unique=True)

    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    zone = models.ForeignKey(Zone, on_delete=models.SET_NULL, null=True)
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['courier_choice']),
        ]


class Order(models.Model):
    order_id = models.CharField(primary_key=True, max_length=50)

    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    customer_name = models.CharField(max_length=50)
    customer_phone = models.CharField(max_length=20)
    customer_email = models.EmailField(null=True, blank=True)
    customer_address = models.CharField(max_length=255)
    customer_note = models.CharField(max_length=255, null=True, blank=True)

    courier_choice = models.IntegerField(
        choices=CourierOption.choices, default=CourierOption.PATHAO)
    courier_store = models.ForeignKey(
        CourierStore, on_delete=models.SET_NULL, null=True, blank=True)

    customer_city = models.ForeignKey(
        City, on_delete=models.SET_NULL, null=True, blank=True)
    customer_zone = models.ForeignKey(
        Zone, on_delete=models.SET_NULL, null=True, blank=True)
    customer_area = models.ForeignKey(
        Area, on_delete=models.SET_NULL, null=True, blank=True)

    item_quantity = models.IntegerField(default=1)
    item_weight = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.50)
    item_description = models.TextField(null=True, blank=True)
    delivery_instruction = models.TextField(null=True, blank=True)

    delivery_type = models.IntegerField(
        choices=DeliveryType.choices,
        default=DeliveryType.REGURAL
    )
    item_type = models.IntegerField(
        choices=ItemType.choices,
        default=ItemType.PARCEL
    )

    products_base_value = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    products_regular_value = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    products_discount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    flat_discount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    additional_discount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    customers_delivery_charge = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)

    amount_to_collect = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    delivery_cost = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    order_profit = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)

    delivery_consignment_id = models.CharField(
        max_length=255, null=True, blank=True)
    delivery_tracking_url = models.CharField(
        max_length=255, null=True, blank=True)

    payment_method = models.IntegerField(
        choices=PaymentMethod.choices,
        default=PaymentMethod.CASH_ON_DELIVERY
    )

    order_status = models.IntegerField(
        choices=OrderStatus.choices,
        default=OrderStatus.PROCESSING
    )
    payment_status = models.IntegerField(
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING
    )

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    @staticmethod
    def generate_order_id(user_phone):
        company_prefix = 'F'
        date_prefix = datetime.datetime.now().strftime('%Y%m%d')
        random_chars = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=4)
        )
        return f"{company_prefix}{date_prefix}-{random_chars}-{user_phone[-4:]}"

    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = self.generate_order_id(
                self.customer.phone_number[-4:])
        super().save(*args, **kwargs)

    class Meta:
        indexes = [
            models.Index(fields=['order_id']),
            models.Index(fields=['customer']),
            models.Index(fields=['order_status']),
            models.Index(fields=['payment_status'])
        ]


class OrderedProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_size = models.CharField(max_length=10)
    product_price = models.IntegerField(default=0)
    product_quantity = models.IntegerField(default=1)

    class Meta:
        indexes = [
            models.Index(fields=['order']),
            models.Index(fields=['product']),
        ]


class OrderNote(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        indexes = [
            models.Index(fields=['order']),
            models.Index(fields=['title']),
        ]


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    description = models.TextField()
    is_approved = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        indexes = [
            models.Index(fields=['order']),
            models.Index(fields=['product']),
            models.Index(fields=['is_approved']),
        ]
