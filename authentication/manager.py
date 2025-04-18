from django.contrib.auth.base_user import BaseUserManager
from .enums import StaffLevel


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('phone number is required')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone_number, password, full_name, email, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('staff_level', StaffLevel.MANAGER)
        extra_fields.setdefault('full_name', full_name)
        extra_fields.setdefault('email', email)
        return self.create_user(phone_number, password, **extra_fields)
