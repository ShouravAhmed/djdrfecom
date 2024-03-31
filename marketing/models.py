import blurhash
from django.apps import apps
from django.db import models

from product.models import Product

from .enums import OfferType


class Banner(models.Model):
    title = models.CharField(max_length=100, unique=True)
    image = models.ImageField(null=True, blank=True)
    image_blurhash = models.CharField(max_length=100, blank=True, null=True)
    redirect_url = models.CharField(max_length=255)
    banner_order = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.image_blurhash = blurhash.encode(
            self.image.open(), x_components=6, y_components=3)
        super().save(*args, **kwargs)

    class Meta:
        indexes = [
            models.Index(fields=['title']),
        ]


class Offer(models.Model):
    offer_type = models.IntegerField(choices=OfferType.choices)
    title = models.CharField(max_length=100)
    description = models.TextField()

    cover_image = models.ImageField(null=True, blank=True)
    cover_image_blurhash = models.CharField(
        max_length=100, blank=True, null=True)
    redirect_url = models.CharField(max_length=255)

    sms_notify = models.BooleanField()
    email_notify = models.BooleanField()
    app_notify = models.BooleanField()

    notification_frequency_day = models.IntegerField()
    sms_frequency_day = models.IntegerField()
    duration_day = models.IntegerField()
    promo_code = models.CharField(max_length=50)

    minimum_purchase = models.IntegerField()
    DiscountPercentage = models.IntegerField()

    def save(self, *args, **kwargs):
        self.cover_image_blurhash = blurhash.encode(
            self.cover_image.open(), x_components=6, y_components=3)
        super().save(*args, **kwargs)

    class Meta:
        indexes = [
            models.Index(fields=['offer_type']),
            models.Index(fields=['title']),
            models.Index(fields=['duration_day']),
            models.Index(fields=['promo_code']),
        ]


class OfferProduct(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=['offer']),
            models.Index(fields=['product']),
        ]


class Notification(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    cover_image = models.ImageField(null=True, blank=True)
    cover_image_blurhash = models.CharField(
        max_length=100, blank=True, null=True)
    redirect_url = models.CharField(max_length=255)

    sms_notify = models.BooleanField()
    email_notify = models.BooleanField()
    app_notify = models.BooleanField()

    notification_frequency_day = models.IntegerField()
    sms_frequency_day = models.IntegerField()

    expire_on = models.DateTimeField()

    def save(self, *args, **kwargs):
        self.cover_image_blurhash = blurhash.encode(
            self.cover_image.open(), x_components=6, y_components=3)
        super().save(*args, **kwargs)

    class Meta:
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['expire_on']),
        ]


class NotificationProduct(models.Model):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=['notification']),
            models.Index(fields=['product']),
        ]
