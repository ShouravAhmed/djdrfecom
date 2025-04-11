import os

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from dotenv import load_dotenv
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

load_dotenv()

admin_url = os.environ.get('ADMIN_URL')

urlpatterns = [
    path(admin_url, admin.site.urls),
    path('api/auth/', include('authentication.urls')),
    path('api/product/', include('product.urls')),
    path('api/marketing/', include('marketing.urls')),
    path('api/order/', include('order.urls')),

    # API Documentation
    path('api/schema/download', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/',
         SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
