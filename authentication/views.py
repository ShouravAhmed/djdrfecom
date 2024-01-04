from django.contrib.auth import authenticate
from django_ratelimit.decorators import ratelimit
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from common.utils import is_valid_password

from .helper import send_login_otp
from .models import User
from .serializers import UserSerializer


@ratelimit(key='user_or_ip', rate='5/d')
@ratelimit(key='user_or_ip', rate='1/m')
@api_view(['POST'])
def send_otp(request):
    try:
        if 'phone_number' not in request.data:
            return Response(
                {"data": "phone number required."},
                status=status.HTTP_404_NOT_FOUND
            )

        phone_number = request.data.get('phone_number')
        user, created = User.objects.get_or_create(phone_number=phone_number)

        data = send_login_otp(phone_number)
        return Response(
            data,
            status=status.HTTP_200_OK
        )

    except Exception as e:
        print(e)
        return Response({"data": "exception occered", }, status=status.HTTP_404_NOT_FOUND)


@ratelimit(key='user_or_ip', rate='20/m')
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_user(request):
    resp = {'status': 200, 'message': 'success'}
    try:
        user = request.user
        serializer = UserSerializer(user, many=False)
        resp['user'] = serializer.data

    except Exception as e:
        resp['message'] = 'Exception Occered'
        resp['exception'] = str(e)

    return Response(resp, status=status.HTTP_200_OK)


@ratelimit(key='user_or_ip', rate='10/m')
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def update_user(request):
    resp = {'status': 200, 'message': 'success'}
    try:
        phone_number = request.user.phone_number
        full_name = request.data.get('full_name')
        email = request.data.get('email')
        address = request.data.get('address')

        user = User.objects.filter(phone_number=phone_number).update(
            full_name=full_name, email=email, address=address)

        serializer = UserSerializer(user, many=False)
        resp['user'] = serializer.data

    except Exception as e:
        resp['message'] = 'Exception Occered'
        resp['exception'] = str(e)

    return Response(resp, status=status.HTTP_200_OK)


@ratelimit(key='user_or_ip', rate='10/m')
@api_view(['POST'])
@permission_classes((IsAuthenticated, IsAdminUser))
def update_admin(request):
    if request.user.staff_level != 5:
        raise PermissionDenied("You do not have permission to access this")

    resp = {'status': 200, 'message': 'success'}
    try:
        manager_phone_number = request.user.phone_number
        manager_password = request.data.get('manager_password', '')
        staff_phone_number = request.data.get('phone_number')
        staff_full_name = request.data.get('full_name', 'Admin')
        staff_level = request.data.get('staff_level', 1)
        staff_password = request.data.get('new_password', '')
        staff_confirm_password = request.data.get('confirm_new_password', '')

        if authenticate(username=manager_phone_number, password=manager_password):
            user, created = User.objects.get_or_create(
                phone_number=staff_phone_number)
            user.full_name = staff_full_name
            user.staff_level = staff_level
            user.is_staff = True
            user.is_varified = True
            if is_valid_password(staff_password, staff_confirm_password):
                user.set_password(staff_password)
            user.save()

            resp['toast'] = f"Admin {'Created' if created else 'Updated'} Successfully"

        admin_list = User.objects.filter(is_staff=True)
        serializer = UserSerializer(admin_list, many=True)
        resp['admin_list'] = serializer.data

    except Exception as e:
        resp['message'] = 'Exception Occered'
        resp['exception'] = str(e)

    return Response(resp, status=status.HTTP_200_OK)


@ratelimit(key='user_or_ip', rate='10/m')
@api_view(['GET'])
@permission_classes((IsAuthenticated, IsAdminUser))
def get_admin_list(request):
    if request.user.staff_level != 5:
        raise PermissionDenied("You do not have permission to access this")

    resp = {'status': 200, 'message': 'success'}
    try:
        admin_list = User.objects.filter(is_staff=True)

        serializer = UserSerializer(admin_list, many=True)
        resp['admin_list'] = serializer.data

    except Exception as e:
        resp['message'] = 'Exception Occered'
        resp['exception'] = str(e)

    return Response(resp, status=status.HTTP_200_OK)
