from django.db import models

from authentication.models import User
from common.pathao import PathaoApi
from common.utils import OrderIDGenerator
from product.models import Product, Store

from .enums import CourierOption, DeliveryType, ItemType, PaymentMethod
from .manager import OrderManager


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


class Store(models.Model):
    store_manager = models.ForeignKey(User, on_delete=models.SET_NULL)
    store_name = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=30)
    second_contact_number = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.store_name

    class Meta:
        indexes = [
            models.Index(fields=['store_name']),
        ]


class CourierStore(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    courier_choice = models.IntegerField(choices=CourierOption.choices)
    courier_store_id = models.IntegerField(primary_key=True, unique=True)

    city = models.ForeignKey(City, on_delete=models.SET_NULL)
    zone = models.ForeignKey(Zone, on_delete=models.SET_NULL)
    area = models.ForeignKey(Area, on_delete=models.SET_NULL)

    class Meta:
        indexes = [
            models.Index(fields=['courier_choice']),
        ]


class Order(models.Model):
    order_id = models.CharField(primary_key=True, max_length=50)
    customer = models.ForeignKey(User, on_delete=models.SET_NULL)

    created_at = models.DateField(auto_now_add=True, editable=False)
    updated_at = models.DateField(auto_now=True, editable=False)

    customer_name = models.CharField(max_length=50)
    customer_phone = models.CharField(max_length=20)
    customer_email = models.EmailField(null=True, blank=True)
    customer_address = models.CharField(max_length=255)
    note = models.CharField(max_length=255)

    courier_choice = models.IntegerField(choices=CourierOption.choices)
    courier_store = models.ForeignKey(CourierStore, on_delete=models.SET_NULL)

    customer_city = models.ForeignKey(City, on_delete=models.SET_NULL)
    customer_zone = models.ForeignKey(Zone, on_delete=models.SET_NULL)
    customer_area = models.ForeignKey(Area, on_delete=models.SET_NULL)

    products_value = models.DecimalField(max_digits=10, decimal_places=2)
    order_value = models.DecimalField(max_digits=10, decimal_places=2)

    item_quantity = models.PositiveBigIntegerField(default=1)
    item_weight = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.50
    )
    item_description = models.TextField()
    delivery_instruction = models.TextField()

    delivery_type = models.IntegerField(
        choices=DeliveryType.choices,
        default=DeliveryType.REGURAL
    )
    item_type = models.IntegerField(
        choices=ItemType.choices,
        default=ItemType.PARCEL
    )

    delivery_cost = models.PositiveBigIntegerField(default=0)
    amount_to_collect = models.PositiveBigIntegerField(default=0)

    delivery_consignment_id = models.CharField(255)
    delivery_tracking_url = models.CharField(255)

    payment_method = models.IntegerField(
        choices=PaymentMethod.choices,
        default=PaymentMethod.CASH_ON_DELIVERY
    )

    order_status = models.CharField(max_length=50)
    payment_status = models.BooleanField()
    profit = models.DecimalField(max_digits=3, decimal_places=2)

    objects = OrderManager()

    def save(self, *args, **kwargs):
        if self.order_id is None:
            self.order_id = self.objects.generate_order_id(
                self.customer.phone_number[-4:]
            )
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
    product = models.ForeignKey(Product, on_delete=models.SET_NULL)
    product_size = models.CharField(max_length=10)
    product_quantity = models.PositiveBigIntegerField(default=1)

    class Meta:
        indexes = [
            models.Index(fields=['order']),
            models.Index(fields=['product']),
        ]


class OrderNote(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField()

    class Meta:
        indexes = [
            models.Index(fields=['order']),
            models.Index(fields=['title']),
        ]


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    description = models.TextField()
    is_approved = models.BooleanField()

    class Meta:
        indexes = [
            models.Index(fields=['order']),
            models.Index(fields=['product']),
            models.Index(fields=['is_approved']),
        ]
