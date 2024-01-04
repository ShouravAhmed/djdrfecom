from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import *

urlpatterns = [
    path('send-otp/', send_otp, name='send_otp'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('get-user/', get_user, name='get_user'),
    path('update-user/', update_user, name='update_user'),

    path('update-admin/', update_admin, name='update_admin'),
    path('get-admin-list/', get_admin_list, name='get_admin_list'),
]
