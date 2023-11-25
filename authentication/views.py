from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .helper import send_login_otp
from .models import User
from .serializers import UserSerializer


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


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def update_user(request):
    resp = {'status': 200, 'message': 'success'}
    try:
        phone_number = request.data.get('phone_number')
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
