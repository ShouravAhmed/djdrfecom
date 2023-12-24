from django.core.cache import cache
from django.utils.translation import gettext as _
from rest_framework import serializers

from .models import User

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.cache import cache


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ['phone_number', 'full_name',
                  'address', 'email', 'points', 'date_joined', 'staff_level', 'is_staff']


class LoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['phone_number'] = user.phone_number
        return token

    phone_number = serializers.CharField(write_only=True)
    otp = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        phone_number = attrs.get('phone_number', None)
        otp = attrs.get('otp', None)

        if not phone_number or not otp:
            raise serializers.ValidationError(
                _("Phone number and OTP are required."), code='authorization')

        user = User.objects.filter(phone_number=phone_number).first()
        if not user:
            raise serializers.ValidationError(
                _("Phone number is not correct."), code='authorization')

        otp_cache_key = f'OTP_{phone_number}'
        cached_otp = cache.get(otp_cache_key, None)

        if (cached_otp != otp):
            raise serializers.ValidationError(
                _("OTP is not correct."), code='authorization')

        refresh = RefreshToken.for_user(user)
        serializer = UserSerializer(user, many=False)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': serializer.data
        }
