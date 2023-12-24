import random

from django.apps import apps
from django.core.exceptions import ValidationError
from django.db import models

from authentication.models import User


class ProductCategory(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    cover_picture = models.CharField(max_length=255)
    profile_picture = models.CharField(max_length=255)
    show_in_home_page = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(fields=['id']),
        ]

    def __str__(self):
        return self.title


class ProductDescription(models.Model):
    product_category = models.ForeignKey(
        ProductCategory, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    specification = models.TextField()

    def __str__(self):
        return f"{self.product_category.title} : {self.title}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['product_category', 'title'],
                name='unique_product_description'
            ),
        ]
        indexes = [
            models.Index(fields=['product_category']),
            models.Index(fields=['id']),
        ]


class ProductSizeChart(models.Model):
    product_category = models.ForeignKey(
        ProductCategory, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    size_chart = models.JSONField()

    def __str__(self):
        return f"{self.product_category.title} : {self.title}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['product_category', 'title'],
                name='unique_product_size_chart'
            ),
        ]
        indexes = [
            models.Index(fields=['product_category']),
            models.Index(fields=['id']),
        ]


class Store(models.Model):
    store_manager = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True)
    store_name = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=30)
    second_contact_number = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.store_name

    class Meta:
        indexes = [
            models.Index(fields=['id']),
        ]


class Product(models.Model):
    def generate_unique_product_id():
        return random.randint(100000, 999999)

    product_id = models.PositiveBigIntegerField(
        primary_key=True, unique=True, default=generate_unique_product_id)
    product_category = models.ForeignKey(
        ProductCategory, on_delete=models.SET_NULL, null=True)
    product_description = models.ForeignKey(
        ProductDescription, on_delete=models.SET_NULL, null=True)
    product_size_chart = models.ForeignKey(
        ProductSizeChart, on_delete=models.SET_NULL, null=True)
    store = models.ForeignKey(Store, on_delete=models.SET_NULL, null=True)

    created_at = models.DateField(auto_now_add=True, editable=False)
    updated_at = models.DateField(auto_now=True, editable=False)

    product_name = models.CharField(max_length=100)
    product_buy_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_sell_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_discount = models.DecimalField(max_digits=5, decimal_places=2)

    sale_count = models.IntegerField(default=0)
    visit_count = models.IntegerField(default=0)
    wishlist_count = models.IntegerField(default=0)

    quantity_in_stock = models.JSONField()
    video_url = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.product_name

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['product_id'],
                name='unique_product_id'
            ),
        ]
        indexes = [
            models.Index(fields=['product_id']),
            models.Index(fields=['product_category']),
            models.Index(fields=['product_name']),
        ]


class ProductPhoto(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    photo_url = models.CharField(max_length=255)

    class Meta:
        indexes = [
            models.Index(fields=['product']),
        ]


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def clean(self):
        if not self.name.replace(" ", "").isalpha() or len(self.name) > 30:
            raise ValidationError(
                _('Invalid Tag Name'),
            )
        self.name = self.name.lower().strip()

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=['name']),
        ]


class ProductTag(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=['product']),
            models.Index(fields=['tag']),
        ]


class CartProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True, editable=False)

    class Meta:
        indexes = [
            models.Index(fields=['product']),
            models.Index(fields=['user']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'user'],
                name='unique_cart'
            ),
        ]


class WishListProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True, editable=False)

    class Meta:
        indexes = [
            models.Index(fields=['product']),
            models.Index(fields=['user']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'user'],
                name='unique_wishlist'
            ),
        ]
