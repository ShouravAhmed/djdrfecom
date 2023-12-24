from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.response import Response

from common.services import all_objects, filter_objects, get_object

from .models import (Product, ProductCategory, ProductDescription,
                     ProductSizeChart, Store, ProductPhoto, ProductTag, 
                     CartProduct, WishListProduct)
from .serializers import (ProductCategorySerializer,
                          ProductDescriptionSerializer, ProductSerializer,
                          ProductSizeChartSerializer, StoreSerializer, 
                          ProductPhotoSerializer, ProductTagSerializer,
                          CartProductSerializer, WishListProductSerializer)


class ProductCategoryViewSet(viewsets.ViewSet):
    """
    Viewset for ProductCategory
    """
    queryset = all_objects(ProductCategory.objects,
                           model_name="ProductCategory")

    @extend_schema(responses=ProductCategorySerializer)
    def list(self, request):
        serializer = ProductCategorySerializer(self.queryset, many=True)
        return Response(serializer.data)


class ProductDescriptionViewSet(viewsets.ViewSet):
    """
    Viewset for ProductDescription
    """
    queryset = all_objects(ProductDescription.objects,
                           model_name="ProductDescription")

    @extend_schema(responses=ProductDescriptionSerializer)
    def list(self, request):
        serializer = ProductDescriptionSerializer(self.queryset, many=True)
        return Response(serializer.data)


class ProductSizeChartViewSet(viewsets.ViewSet):
    """
    Viewset for ProductSizeChart
    """
    queryset = all_objects(ProductSizeChart.objects,
                           model_name="ProductSizeChart")

    @extend_schema(responses=ProductSizeChartSerializer)
    def list(self, request):
        serializer = ProductSizeChartSerializer(self.queryset, many=True)
        return Response(serializer.data)


class StoreViewSet(viewsets.ViewSet):
    """
    Viewset for Store
    """
    queryset = all_objects(Store.objects,
                           model_name="Store")

    @extend_schema(responses=StoreSerializer)
    def list(self, request):
        serializer = StoreSerializer(self.queryset, many=True)
        return Response(serializer.data)


class ProductViewSet(viewsets.ViewSet):
    """
    Viewset for Product
    """
    queryset = all_objects(Product.objects,
                           model_name="Product")

    @extend_schema(responses=ProductSerializer)
    def list(self, request):
        serializer = ProductSerializer(self.queryset, many=True)
        return Response(serializer.data)

class ProductPhotoViewSet(viewsets.ViewSet):
    """
    Viewset for ProductPhoto
    """
    queryset = all_objects(ProductPhoto.objects,
                           model_name="ProductPhoto")

    @extend_schema(responses=ProductPhotoSerializer)
    def list(self, request):
        serializer = ProductPhotoSerializer(self.queryset, many=True)
        return Response(serializer.data)
    
    
class ProductTagViewSet(viewsets.ViewSet):
    """
    Viewset for ProductTag
    """
    queryset = all_objects(ProductTag.objects,
                           model_name="ProductTag")

    @extend_schema(responses=ProductTagSerializer)
    def list(self, request):
        serializer = ProductTagSerializer(self.queryset, many=True)
        return Response(serializer.data)

class CartProductViewSet(viewsets.ViewSet):
    """
    Viewset for CartProduct
    """
    queryset = all_objects(CartProduct.objects,
                           model_name="CartProduct")

    @extend_schema(responses=CartProductSerializer)
    def list(self, request):
        serializer = CartProductSerializer(self.queryset, many=True)
        return Response(serializer.data)

class WishListProductViewSet(viewsets.ViewSet):
    """
    Viewset for WishListProduct
    """
    queryset = all_objects(WishListProduct.objects,  
                           model_name="WishListProduct")

    @extend_schema(responses=WishListProductSerializer)
    def list(self, request):
        serializer = WishListProductSerializer(self.queryset, many=True)
        return Response(serializer.data)
      