from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response

from common.services import (all_objects, delete_objects, filter_objects,
                             get_object)

from .models import (CartProduct, Product, ProductCategory, ProductDescription,
                     ProductPhoto, ProductSizeChart, ProductTag, Store,
                     WishListProduct)
from .serializers import (CartProductSerializer, ProductCategorySerializer,
                          ProductDescriptionSerializer, ProductPhotoSerializer,
                          ProductSerializer, ProductSizeChartSerializer,
                          ProductTagSerializer, StoreSerializer,
                          WishListProductSerializer)


class ProductCategoryViewSet(viewsets.ViewSet):
    """
    Viewset for ProductCategory
    """
    queryset = all_objects(ProductCategory.objects,
                           model_name="ProductCategory")

    @extend_schema(responses=ProductCategorySerializer)
    def list(self, request):
        """
        An endpoint to return all product categories
        """
        serializer = ProductCategorySerializer(self.queryset, many=True)
        return Response(serializer.data)

    @extend_schema(request=ProductCategorySerializer, responses=ProductCategorySerializer)
    @permission_classes([permissions.IsAuthenticated, permissions.IsAdminUser])
    def create(self, request):
        """
        An endpoint to create a product category
        """
        serializer = ProductCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(request=ProductCategorySerializer, responses=ProductCategorySerializer)
    @permission_classes([permissions.IsAuthenticated, permissions.IsAdminUser])
    @action(
        methods=['put'],
        detail=False,
        url_path=r"update/(?P<update_pk>\d+)",
        url_name="update_product_category"
    )
    def update_category(self, request, update_pk=None):
        """
        An endpoint to update a product category
        """
        instance = get_object(self.queryset, pk=update_pk)
        serializer = ProductCategorySerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(responses={status.HTTP_204_NO_CONTENT: None})
    @permission_classes([permissions.IsAuthenticated, permissions.IsAdminUser])
    @action(
        methods=['delete'],
        detail=False,
        url_path=r"delete/(?P<delete_pk>\d+)",
        url_name="delete_product_category"
    )
    def delete_category(self, request, delete_pk=None):
        """
        An endpoint to delete a product category
        """
        instance = get_object(self.queryset, pk=delete_pk)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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

    @extend_schema(responses=ProductSerializer)
    @action(
        methods=['get'],
        detail=False,
        url_path=r"category/(?P<category>\w+)/all",
        url_name="product_by_category"
    )
    def list_product_by_category(self, request, category=None):
        """
        An endpoint to return products by category
        """
        serializer = ProductSerializer(
            filter_objects(self.queryset, product_category=category), many=True)
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
    @permission_classes([permissions.IsAuthenticated, permissions.IsAdminUser])
    def list(self, request):
        """
        An endpoint to return all product Tags
        """
        serializer = ProductTagSerializer(self.queryset, many=True)
        return Response(serializer.data)

    @extend_schema(responses=ProductTagSerializer)
    @permission_classes([permissions.IsAuthenticated, permissions.IsAdminUser])
    def create(self, request):
        """
        An endpoint to create a product Tag
        """
        serializer = ProductTagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(responses={status.HTTP_204_NO_CONTENT: None})
    @permission_classes([permissions.IsAuthenticated, permissions.IsAdminUser])
    @action(
        methods=['delete'],
        detail=False,
        url_path=r"delete/(?P<delete_pk>\d+)",
        url_name="delete_product_tag"
    )
    def delete_tag(self, request, delete_pk=None):
        """
        An endpoint to delete a product tag
        """
        instance = get_object(self.queryset, pk=delete_pk)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartProductViewSet(viewsets.ViewSet):
    """
    Viewset for CartProduct
    """
    queryset = all_objects(CartProduct.objects, model_name="CartProduct")

    @extend_schema(responses=CartProductSerializer)
    @permission_classes([permissions.IsAuthenticated])
    def list(self, request):
        """
        An endpoint to retrieve items in the user's Cart
        """
        cart_products = filter_objects(
            self.queryset, user=request.user, model_name="CartProduct")
        serializer = CartProductSerializer(cart_products, many=True)
        return Response(serializer.data)

    @extend_schema(responses=CartProductSerializer)
    @permission_classes([permissions.IsAuthenticated])
    @action(
        methods=['post'],
        detail=False,
        url_path=r"update",
        url_name="update_cart"
    )
    def update_cart(self, request):
        """
        An endpoint to update items in the user's Cart
        """
        cart_products = filter_objects(
            self.queryset, user=request.user, model_name="CartProduct")
        delete_objects(cart_products, model_name="CartProduct")

        products_data = request.data.get('products', [])
        response_data = []

        for product_data in products_data:
            data = {
                'product': product_data.product_id,
                'user': request.user.id
            }
            serializer = CartProductSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                response_data.append(serializer.data)

        return Response(response_data, status=status.HTTP_201_CREATED)


class WishListProductViewSet(viewsets.ViewSet):
    """
    Viewset for WishListProduct
    """
    queryset = all_objects(WishListProduct.objects,
                           model_name="WishListProduct")

    @extend_schema(responses=WishListProductSerializer)
    @permission_classes([permissions.IsAuthenticated])
    def list(self, request):
        """
        An endpoint to retrieve items in the user's wishlist
        """
        wishlist_products = filter_objects(
            self.queryset, user=request.user, model_name="WishListProduct")
        serializer = WishListProductSerializer(wishlist_products, many=True)
        return Response(serializer.data)

    @extend_schema(responses=WishListProductSerializer)
    @permission_classes([permissions.IsAuthenticated])
    @action(
        methods=['post'],
        detail=False,
        url_path=r"update",
        url_name="update_wishlist"
    )
    def update_wishlist(self, request):
        """
        An endpoint to update items in the user's wishlist
        """
        wishlist_products = filter_objects(
            self.queryset, user=request.user, model_name="WishListProduct")
        delete_objects(wishlist_products, model_name="WishListProduct")

        products_data = request.data.get('products', [])
        response_data = []

        for product_data in products_data:
            data = {
                'product': product_data.product_id,
                'user': request.user.id
            }
            serializer = WishListProductSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                response_data.append(serializer.data)

        return Response(response_data, status=status.HTTP_201_CREATED)
