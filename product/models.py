import datetime
import random
import re
import string

import blurhash
from django.apps import apps
from django.core.exceptions import ValidationError
from django.db import models

from authentication.models import User
from common.utils import get_slug


def generate_unique_id():
    current_year = str(datetime.datetime.now().year)[-2:]
    current_month = str(datetime.datetime.now().month).zfill(2)
    current_day = str(datetime.datetime.now().day).zfill(2)

    random_number1 = str(random.randint(100, 999))
    random_chars1 = ''.join(random.choices(
        string.ascii_uppercase, k=2))
    random_number2 = str(random.randint(100, 999))
    random_chars2 = ''.join(random.choices(
        string.ascii_uppercase, k=2))
    return f"{current_year}{current_month}{current_day}{random_number1}{random_chars1}{random_number2}{random_chars2}"


class ProductCategory(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)

    cover_image = models.ImageField(null=True, blank=True)
    cover_image_blurhash = models.CharField(
        max_length=100, blank=True, null=True)

    profile_image = models.ImageField(null=True, blank=True)
    profile_image_blurhash = models.CharField(
        max_length=100, blank=True, null=True)

    show_in_home_page = models.BooleanField(default=True)
    two_in_a_row = models.BooleanField(default=False)

    category_order = models.IntegerField(default=0)
    slug = models.CharField(max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = get_slug(self.title)

        self.cover_image_blurhash = blurhash.encode(
            self.cover_image.open(), x_components=6, y_components=3)

        self.profile_image_blurhash = blurhash.encode(
            self.profile_image.open(), x_components=6, y_components=3)

        super().save(*args, **kwargs)

    class Meta:
        indexes = [
            models.Index(fields=['id', 'title']),
        ]
        ordering = ['category_order']

    def __str__(self):
        return self.title + " | " + str(self.category_order)


class ProductDescription(models.Model):
    product_category = models.ForeignKey(
        ProductCategory, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    specification = models.TextField()

    slug = models.CharField(max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = get_slug(self.title)
        super().save(*args, **kwargs)

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

    slug = models.CharField(max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = get_slug(self.title)
        super().save(*args, **kwargs)

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
    store_name = models.CharField(max_length=50, unique=True)
    contact_number = models.CharField(max_length=30)
    second_contact_number = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    slug = models.CharField(max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = get_slug(self.store_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.store_name

    class Meta:
        indexes = [
            models.Index(fields=['id']),
        ]


class Product(models.Model):
    def generate_unique_product_id():
        current_year = str(datetime.datetime.now().year)[-2:]
        current_month = str(datetime.datetime.now().month).zfill(2)
        random_number = str(random.randint(1000, 9999))
        random_chars = ''.join(random.choices(
            string.ascii_uppercase, k=1))
        return f"F{current_year}{current_month}{random_number}{random_chars}"

    product_id = models.CharField(max_length=30,
                                  primary_key=True, unique=True, default=generate_unique_product_id)
    product_category = models.ForeignKey(
        ProductCategory, on_delete=models.SET_NULL, null=True, blank=True)
    product_description = models.ForeignKey(
        ProductDescription, on_delete=models.SET_NULL, null=True, blank=True)
    product_size_chart = models.ForeignKey(
        ProductSizeChart, on_delete=models.SET_NULL, null=True, blank=True)
    store = models.ForeignKey(
        Store, on_delete=models.SET_NULL, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    product_name = models.CharField(max_length=100)
    product_base_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=None, null=True, blank=True)
    product_selling_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=None, null=True, blank=True)
    product_discount = models.DecimalField(
        max_digits=5, decimal_places=2, default=None, null=True, blank=True)

    product_sale_count = models.IntegerField(default=0)
    product_visit_count = models.IntegerField(default=0)
    product_wishlist_count = models.IntegerField(default=0)

    total_stock = models.IntegerField(default=0)
    video_url = models.CharField(max_length=100, null=True, blank=True)

    is_archived = models.BooleanField(default=False)

    profile_image = models.ImageField(null=True, blank=True)
    profile_image_blurhash = models.CharField(
        max_length=100, blank=True, null=True)

    slug = models.CharField(max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.profile_image:
            self.profile_image_blurhash = blurhash.encode(
                self.profile_image.open(), x_components=6, y_components=3)
        self.slug = get_slug(self.product_name)
        super().save(*args, **kwargs)

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


class ProductStock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=10)
    count = models.IntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'size'],
                name='unique_product_stock'
            ),
        ]

    def __str__(self):
        return f"{self.size} : {self.count} : {self.product.product_name}"


class ProductImage(models.Model):
    image_id = models.CharField(
        max_length=30,
        primary_key=True,
        unique=True,
        default=generate_unique_id
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    image_order = models.IntegerField(default=0)
    image_blurhash = models.CharField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.image_blurhash = blurhash.encode(
            self.image.open(), x_components=6, y_components=3)
        super().save(*args, **kwargs)

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
        self.full_clean()
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

    def __str__(self):
        return f"{self.tag.name} : {self.product.product_name}"


class CartProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    size = models.CharField(max_length=30, default="default")
    count = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'user', 'size'],
                name='unique_cart_product'
            ),
        ]

    def __str__(self):
        return f"{self.user.phone_number} : {self.product.product_name}"


class WishListProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        indexes = [
            models.Index(fields=['product']),
            models.Index(fields=['user']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'user'],
                name='unique_wishlist_product'
            ),
        ]
