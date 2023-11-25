from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.response import Response

from common.services import all_objects, filter_objects, get_object

from .models import ProductCategory
from .serializers import ProductCategorySerializer


class ProductCategoryViewSet(viewsets.ViewSet):
    """
    Viewset for ProductCategory
    """
    queryset = all_objects("ProductCategory", ProductCategory.objects)

    @extend_schema(responses=ProductCategorySerializer)
    def list(self, request):
        serializer = ProductCategorySerializer(self.queryset, many=True)
        return Response(serializer.data)
