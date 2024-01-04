from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('fabricraft-super-admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls')),
    path('api/product/', include('product.urls')),

    # API Documentation
    path('api/schema/download', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/',
         SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
