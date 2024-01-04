from datetime import datetime, timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models

from .enums import StaffLevel
from .manager import UserManager


class User(AbstractUser):
    id = models.CharField(max_length=15, default="")
    phone_number = models.CharField(
        max_length=15, unique=True, primary_key=True)
    full_name = models.CharField(max_length=73, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    total_purchase = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    visit_count = models.IntegerField(default=0)

    staff_level = models.IntegerField(
        choices=StaffLevel.choices, default=StaffLevel.USER)

    created_at = models.DateField(auto_now_add=True, editable=False)
    updated_at = models.DateField(auto_now=True, editable=False)

    staff_pass_expire_at = models.DateField(null=True, blank=True)
    is_varified = models.BooleanField(default=False)

    username = models.CharField(max_length=30, null=True, blank=True)

    def set_password(self, raw_password):
        self.staff_pass_expire_at = datetime.now() + timedelta(days=30)
        super().set_password(raw_password)

    def save(self, *args, **kwargs):
        self.id = self.phone_number
        self.username = self.phone_number
        super(User, self).save(*args, **kwargs)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['full_name', 'email']
    objects = UserManager()

    class Meta:
        indexes = [
            models.Index(fields=['phone_number']),
            models.Index(fields=['staff_level']),
        ]
