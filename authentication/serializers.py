from datetime import datetime

from django.contrib.auth import authenticate
from django.core.cache import cache
from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from common.utils import is_valid_password

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ['phone_number', 'full_name',
                  'address', 'email', 'points', 'date_joined', 'staff_level', 'is_staff', 'is_varified']


class LoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['phone_number'] = user.phone_number
        return token

    phone_number = serializers.CharField(write_only=True)
    otp = serializers.CharField(write_only=True)

    def validate(self, attrs):
        phone_number = attrs.get('phone_number', "")
        secret = attrs.get('otp', "").split('-')
        otp, password, new_password, confirm_new_password = [
            secret[i] if i < len(secret) else "" for i in range(4)]

        if phone_number == "" or otp == "":
            raise serializers.ValidationError(
                _("Phone number and OTP is required."), code='authorization')

        user = User.objects.filter(phone_number=phone_number).first()
        if not user:
            raise serializers.ValidationError(
                _("Phone number is not correct."), code='authorization')

        otp_cache_key = f'OTP_{phone_number}'
        cached_otp = cache.get(otp_cache_key, None)

        if (cached_otp != otp):
            raise serializers.ValidationError(
                _("OTP is not correct. Please enter OTP carefully!"), code='authorization')

        # Check if the user is a staff member
        if user.is_staff:
            # If the staff user's password has expired, raise validation error
            if user.staff_pass_expire_at and datetime.combine(user.staff_pass_expire_at, datetime.min.time()) < datetime.now():
                if not is_valid_password(new_password, confirm_new_password):
                    raise serializers.ValidationError(
                        _("Staff password has expired! The new password must be at least 8 characters and include a lowercase letter, an uppercase letter, a digit, and a special character: ~ ! @ # $ % ^ & * - _ + =  | ?"), code='authorization')
                user.set_password(new_password)
                user.save()
                raise serializers.ValidationError(
                    _("Staff password updated successfully! please login!!"), code='authorization')

            # Authenticate staff user using password
            if not authenticate(username=user.username, password=password):
                raise serializers.ValidationError(
                    _("Staff requires a correct password to login!"), code='authorization')

        if not user.is_varified:
            user.is_varified = True
            user.save()

        refresh = RefreshToken.for_user(user)
        serializer = UserSerializer(user, many=False)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': serializer.data
        }
