import logging

from django.contrib.auth import authenticate
from django.core.cache import cache
from django.db import transaction
from django.db.models import F, Func, Sum, Value
from django.forms.models import model_to_dict
from django.shortcuts import render
from django.utils.translation import gettext as _
from django_ratelimit.decorators import ratelimit
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, serializers, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response

from authentication.models import User
from common.services import (all_objects, delete_objects, filter_objects,
                             get_object)

from .models import (CartProduct, Product, ProductCategory, ProductDescription,
                     ProductImage, ProductSizeChart, ProductStock, ProductTag,
                     Store, Tag, WishListProduct)
from .serializers import (CartProductSerializer, ProductCategorySerializer,
                          ProductDescriptionSerializer, ProductImageSerializer,
                          ProductSerializer, ProductSizeChartSerializer,
                          ProductTagSerializer, StoreSerializer,
                          WishListProductSerializer)
from .utils import ProductCategoryCache

logger = logging.getLogger('main')


@ratelimit(key='user_or_ip', rate='60/m')
@api_view(['GET'])
def homepage_products(request):
    if data := cache.get("HOMEPAGE_PRODUCTS"):
        return Response(data, status=status.HTTP_200_OK)

    categories = ProductCategory.objects.filter(show_in_home_page=True)
    data = {}
    for category in categories:
        products = Product.objects.filter(
            product_category=category,
            is_archived=False,
            total_stock__gt=0
        )
        products = products.annotate(
            popularity_value=F('product_sale_count') * 10 +
            F('product_visit_count') + F('product_wishlist_count') * 2,
        )
        products = products.order_by('-popularity_value', '-total_stock')[:6]
        serialized_products = ProductSerializer(products, many=True).data
        data[category.title] = serialized_products

    cache.set("HOMEPAGE_PRODUCTS", data, 7200)
    return Response(data, status=status.HTTP_200_OK)


@ratelimit(key='user_or_ip', rate='60/m')
@api_view(['GET'])
def shop_products(request, query=None):
    try:
        if query == 'undefined':
            query = None

        if data := cache.get(f"SHOP_PRODUCTS_{query}"):
            return Response(data, status=status.HTTP_200_OK)

        if not query:
            products = all_objects(Product.objects, model_name="Product")
            products = products.order_by('?')

            serializer = ProductSerializer(products.distinct(), many=True)
            cache.set(f"SHOP_PRODUCTS_{query}", serializer.data, 7200)
            return Response(serializer.data, status=status.HTTP_200_OK)

        keywords = query.split('&')
        products = Product.objects.none()

        for keyword in keywords:
            # products_by_name = Product.objects.filter(
            #     product_name__icontains=keyword)
            products_by_tag = Product.objects.filter(
                producttag__tag__name__icontains=keyword)
            products_by_category = Product.objects.filter(
                product_category__title__icontains=keyword)

            products = products | products_by_tag | products_by_category

        products = products.order_by('?')
        serializer = ProductSerializer(products.distinct(), many=True)

        cache.set(f"SHOP_PRODUCTS_{query}", serializer.data, 7200)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({}, status=status.HTTP_200_OK)


@ratelimit(key='user_or_ip', rate='60/m')
@api_view(['GET'])
def search_products(request):
    search_text = request.query_params.get('search', '').strip()
    print("\n\nsearching:", search_text)

    if not search_text:
        return Response({}, status=status.HTTP_200_OK)

    if data := cache.get(f"SEARCH_PRODUCTS_{search_text}"):
        return Response(data, status=status.HTTP_200_OK)

    products_by_name = Product.objects.filter(
        product_name__icontains=search_text)

    products_by_tag = Product.objects.filter(
        producttag__tag__name__icontains=search_text)

    products_by_category = Product.objects.filter(
        product_category__title__icontains=search_text
    )

    products = products_by_name | products_by_tag | products_by_category
    serializer = ProductSerializer(products.distinct(), many=True)

    cache.set(f"SEARCH_PRODUCTS_{search_text}", serializer.data, 7200)
    return Response(serializer.data, status=status.HTTP_200_OK)


class ProductCategoryViewSet(viewsets.ViewSet):
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    cache_provider = ProductCategoryCache()
    queryset = all_objects(ProductCategory.objects,
                           model_name="ProductCategory")

    def __fix_category_order(self):
        categories = all_objects(
            ProductCategory.objects, model_name="ProductCategory")
        sorted_categories = sorted(categories, key=lambda x: x.category_order)

        with transaction.atomic():
            for order, category in enumerate(sorted_categories, start=1):
                category.category_order = order
                category.save()

    def __update_category_order(self, order):
        categories = all_objects(
            ProductCategory.objects, model_name="ProductCategory")

        with transaction.atomic():
            for category in categories:
                category.category_order = order[category.title]
                category.save()

    @extend_schema(responses=ProductCategorySerializer(many=True))
    def list(self, request):
        """Return all product categories."""
        return Response(self.cache_provider.get_product_categories(), status=status.HTTP_200_OK)

    @extend_schema(responses=ProductCategorySerializer)
    @permission_classes([permissions.IsAuthenticated, permissions.IsAdminUser])
    def create(self, request):
        """An endpoint to create a product category"""
        if not authenticate(username=request.user.username, password=request.data.get('admin_password', '')):
            return Response({'message': 'Admin Password Required'}, status=status.HTTP_401_UNAUTHORIZED)

        request_data = request.data.copy()

        if isinstance(request_data.get('cover_image', ''), str):
            del request_data['cover_image']
        if isinstance(request_data.get('profile_image', ''), str):
            del request_data['profile_image']

        category_id = request_data.get('id', None)
        category = filter_objects(
            ProductCategory.objects,
            fields={
                'id': category_id,
            },
            model_name='ProductCategory'
        ) if category_id else None

        if category:
            instance = category[0]
            serializer = ProductCategorySerializer(instance, data=request_data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_204_NO_CONTENT)

        else:
            request_data['category_order'] = 1000

            serializer = ProductCategorySerializer(data=request_data)
            if serializer.is_valid():
                serializer.save()
                self.__fix_category_order()
            else:
                return Response(serializer.errors, status=status.HTTP_204_NO_CONTENT)

        return Response(self.cache_provider.update_product_categories(), status=status.HTTP_200_OK)

    @extend_schema(responses=ProductCategorySerializer)
    @permission_classes([permissions.IsAuthenticated, permissions.IsAdminUser])
    @action(detail=False, methods=['post'], url_path="delete", url_name="delete_product_category")
    def delete_category(self, request):
        """Delete a product category."""
        if not authenticate(username=request.user.username, password=request.data.get('admin_password', '')):
            return Response({'message': 'Admin Password Required'}, status=status.HTTP_401_UNAUTHORIZED)

        instance = get_object(
            ProductCategory.objects,
            fields={'pk': request.data.get('pk'), },
            model_name="ProductCategory"
        )
        instance.delete()
        self.__fix_category_order()

        return Response(self.cache_provider.update_product_categories(), status=status.HTTP_200_OK)

    @extend_schema(responses=ProductCategorySerializer)
    @permission_classes([permissions.IsAuthenticated, permissions.IsAdminUser])
    @action(detail=False, methods=['post'], url_path="update-order", url_name="update_product_category_order")
    def update_category_order(self, request):
        """Update the order of product categories."""
        self.__update_category_order(request.data.get('order'))
        return Response(self.cache_provider.update_product_categories(), status=status.HTTP_200_OK)


class ProductDescriptionViewSet(viewsets.ViewSet):
    """
    Viewset for ProductDescription
    """
    queryset = all_objects(ProductDescription.objects,
                           model_name="ProductDescription")

    @extend_schema(responses=ProductDescriptionSerializer)
    @permission_classes([permissions.IsAuthenticated, permissions.IsAdminUser])
    @action(
        methods=['get'],
        detail=False,
        url_path=r"category/(?P<category>[^/]+)",
        url_name="description_by_category"
    )
    def list_description_by_category(self, request, category=None):
        """
        An endpoint to return SizeChart by C ategory
        """
        serializer = ProductDescriptionSerializer(
            filter_objects(
                ProductDescription.objects,
                fields={
                    'product_category__title': category,
                },
                model_name='ProductDescription'
            ),
            many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(responses=ProductDescriptionSerializer)
    @permission_classes([permissions.IsAuthenticated, permissions.IsAdminUser])
    def create(self, request):
        """An endpoint to create and update a product size chart"""
        if not authenticate(username=request.user.username, password=request.data.get('admin_password', '')):
            return Response({'message': 'Admin Password Required'}, status=status.HTTP_401_UNAUTHORIZED)

        description_title = request.data.get('description_title', None)
        description_data = request.data.get('description_data', None)

        if not description_data:
            return Response('Content not provided for size chart', status=status.HTTP_204_NO_CONTENT)

        description = filter_objects(
            ProductDescription.objects,
            fields={
                'title': description_title,
            },
            model_name='ProductDescription'
        )

        if description:
            instance = description[0]
            serializer = ProductDescriptionSerializer(
                instance, data=description_data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_204_NO_CONTENT)

        else:
            serializer = ProductDescriptionSerializer(data=description_data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_204_NO_CONTENT)

        serializer = ProductDescriptionSerializer(
            all_objects(ProductDescription.objects,
                        model_name="ProductDescription"),
            many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(responses=ProductDescriptionSerializer)
    @permission_classes([permissions.IsAuthenticated, permissions.IsAdminUser])
    @action(detail=False, methods=['post'], url_path="delete", url_name="delete_product_description")
    def delete_description(self, request):
        """Delete a product size chart."""
        if not authenticate(username=request.user.username, password=request.data.get('admin_password', '')):
            return Response({'message': 'Admin Password Required'}, status=status.HTTP_401_UNAUTHORIZED)

        instance = get_object(
            ProductDescription.objects,
            fields={'title': request.data.get('description_title'), },
            model_name="ProductDescription"
        )
        instance.delete()

        serializer = ProductDescriptionSerializer(
            all_objects(ProductDescription.objects,
                        model_name="ProductDescription"),
            many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductSizeChartViewSet(viewsets.ViewSet):
    """
    Viewset for ProductSizeChart
    """
    queryset = all_objects(ProductSizeChart.objects,
                           model_name="ProductSizeChart")

    @extend_schema(responses=ProductSizeChartSerializer)
    @permission_classes([permissions.IsAuthenticated, permissions.IsAdminUser])
    @action(
        methods=['get'],
        detail=False,
        url_path=r"category/(?P<category>[^/]+)",
        url_name="size_chart_by_category"
    )
    def list_size_chart_by_category(self, request, category=None):
        """
        An endpoint to return SizeChart by C ategory
        """
        serializer = ProductSizeChartSerializer(
            filter_objects(
                ProductSizeChart.objects,
                fields={
                    'product_category__title': category,
                },
                model_name='ProductSizeChart'
            ),
            many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(responses=ProductSizeChartSerializer)
    @permission_classes([permissions.IsAuthenticated, permissions.IsAdminUser])
    def create(self, request):
        """An endpoint to create and update a product size chart"""
        if not authenticate(username=request.user.username, password=request.data.get('admin_password', '')):
            return Response({'message': 'Admin Password Required'}, status=status.HTTP_401_UNAUTHORIZED)

        size_chart_title = request.data.get('size_chart_title', None)
        size_chart_data = request.data.get('size_chart_data', None)

        if not size_chart_data:
            return Response('Content not provided for size chart', status=status.HTTP_204_NO_CONTENT)

        size_chart = filter_objects(
            ProductSizeChart.objects,
            fields={
                'title': size_chart_title,
            },
            model_name='ProductSizeChart'
        )

        if size_chart:
            instance = size_chart[0]
            serializer = ProductSizeChartSerializer(
                instance, data=size_chart_data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_204_NO_CONTENT)
        else:
            serializer = ProductSizeChartSerializer(data=size_chart_data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_204_NO_CONTENT)

        serializer = ProductSizeChartSerializer(
            all_objects(ProductSizeChart.objects,
                        model_name="ProductSizeChart"),
            many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(responses=ProductSizeChartSerializer)
    @permission_classes([permissions.IsAuthenticated, permissions.IsAdminUser])
    @action(detail=False, methods=['post'], url_path="delete", url_name="delete_product_size_chart")
    def delete_size_chart(self, request):
        """Delete a product size chart."""
        if not authenticate(username=request.user.username, password=request.data.get('admin_password', '')):
            return Response({'message': 'Admin Password Required'}, status=status.HTTP_401_UNAUTHORIZED)

        instance = get_object(
            ProductSizeChart.objects,
            fields={'title': request.data.get('size_chart_title'), },
            model_name="ProductSizeChart"
        )
        instance.delete()

        serializer = ProductSizeChartSerializer(
            all_objects(ProductSizeChart.objects,
                        model_name="ProductSizeChart"),
            many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class StoreViewSet(viewsets.ViewSet):
    """
    Viewset for Store
    """
    queryset = all_objects(Store.objects,
                           model_name="Store")

    @extend_schema(responses=StoreSerializer)
    @permission_classes([permissions.IsAuthenticated, permissions.IsAdminUser])
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
        serializer = ProductSerializer(
            all_objects(Product.objects, model_name="Product"),
            context={'request': request},
            many=True
        )
        return Response(serializer.data)

    @extend_schema(responses=ProductSerializer)
    @permission_classes([permissions.IsAuthenticated, permissions.IsAdminUser])
    @action(
        methods=['post'],
        detail=False,
        url_path="admin-product",
        url_name="admin_product"
    )
    def admin_product_list(self, request, category=None):
        """
        An endpoint to return SizeChart by C ategory
        """
        filter = request.data
        print('filter: ', filter)

        products = all_objects(Product.objects, model_name="Product")
        if searchId := filter.get('searchId', None):
            print('searchId:', searchId)

            products = filter_objects(
                products,
                fields={
                    'product_id': searchId,
                },
                model_name='Product'
            )
        else:
            if searchName := filter.get('searchName', None):
                print('searchName:', searchName)

                products = filter_objects(
                    products,
                    fields={
                        'product_name__icontains': searchName,
                    },
                    model_name='Product'
                )
            if searchCategoryTitle := filter.get('searchCategoryTitle', None):
                print('searchCategoryTitle:', searchCategoryTitle)

                if searchCategoryTitle != 'All Categories':
                    products = filter_objects(
                        products,
                        fields={
                            'product_category__title': searchCategoryTitle,
                        },
                        model_name='Product'
                    )

        serializer = ProductSerializer(
            products,
            context={'request': request},
            many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(responses=ProductSerializer)
    @action(
        methods=['get'],
        detail=False,
        url_path=r"category/(?P<category>[^/]+)",
        url_name="product_by_category"
    )
    def list_product_by_category(self, request, category=None):
        """
        An endpoint to return products by category `slug`
        """
        if data := cache.get(f"CATEGORY_PRODUCTS_{category}"):
            return Response(data, status=status.HTTP_200_OK)

        serializer = ProductSerializer(
            filter_objects(
                all_objects(Product.objects, model_name="Product"),
                context={'request': request},
                fields={
                    'product_category__slug': category,
                },
                model_name='Product'
            ),
            many=True
        )

        cache.set(f"CATEGORY_PRODUCTS_{category}", serializer.data, 7200)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(responses=ProductSerializer)
    @permission_classes([permissions.IsAuthenticated, permissions.IsAdminUser])
    def create(self, request):
        """An endpoint to create and update a product size chart"""
        if not authenticate(username=request.user.username, password=request.data.get('admin_password', '')):
            return Response({'message': 'Admin Password Required'}, status=status.HTTP_401_UNAUTHORIZED)

        product_data = request.data.get('product_data', None)
        if not product_data:
            return Response('Content not provided for size chart', status=status.HTTP_204_NO_CONTENT)

        print("\nproduct_data: ", product_data, "\n")

        product_data['product_base_price'] = float(
            product_data['product_base_price']
        )
        product_data['product_selling_price'] = float(
            product_data['product_selling_price']
        )
        product_data['product_discount'] = float(
            product_data['product_discount']
        )

        category = ProductCategory.objects.get(
            title=product_data['product_category']
        )
        description = ProductDescription.objects.get(
            title=product_data['product_description'],
            product_category__title=product_data['product_category']
        )
        sizechart = ProductSizeChart.objects.get(
            title=product_data['product_size_chart'],
            product_category__title=product_data['product_category']
        )

        stock = product_data.get('product_stock')
        stock = {key: int(value) for key, value in stock.items()}

        product = None
        if product_id := product_data.get('product_id', None):
            product = filter_objects(
                all_objects(Product.objects, model_name="Product"),
                fields={
                    'product_id': product_id,
                },
                model_name='Product'
            )

        print("\nproduct: ", product, "\n")

        if product:
            instance = product[0]
            instance.product_category = category
            instance.product_description = description
            instance.product_size_chart = sizechart

            instance.product_name = product_data.get('product_name')
            instance.product_base_price = product_data.get(
                'product_base_price')
            instance.product_selling_price = product_data.get(
                'product_selling_price')
            instance.product_discount = product_data.get('product_discount')
            instance.is_archived = product_data.get('is_archived')
            instance.video_url = product_data.get('video_url')
            instance.save()

            for key, value in stock.items():
                stock, created = ProductStock.objects.get_or_create(
                    product=instance,
                    size=key
                )
                stock.count = value
                stock.save()
        else:
            instance = Product.objects.create(
                product_category=category,
                product_description=description,
                product_size_chart=sizechart,
                product_name=product_data.get('product_name'),
                product_base_price=product_data.get('product_base_price'),
                product_selling_price=product_data.get(
                    'product_selling_price'),
                product_discount=product_data.get('product_discount'),
                is_archived=product_data.get('is_archived'),
                video_url=product_data.get('video_url')
            )
            instance.save()
            for key, value in stock.items():
                stock, created = ProductStock.objects.get_or_create(
                    product=instance,
                    size=key
                )
                stock.count = value
                stock.save()

        serializer = ProductSerializer(
            all_objects(Product.objects, model_name="Product"),
            context={'request': request},
            many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(responses=ProductSerializer)
    @permission_classes([permissions.IsAuthenticated, permissions.IsAdminUser])
    @action(detail=False, methods=['post'], url_path="delete", url_name="delete_product")
    def delete_product(self, request):
        """Delete a product size chart."""
        if not authenticate(username=request.user.username, password=request.data.get('admin_password', '')):
            return Response({'message': 'Admin Password Required'}, status=status.HTTP_401_UNAUTHORIZED)

        instance = get_object(
            Product.objects,
            fields={'product_id': request.data.get('product_id'), },
            model_name="Product"
        )
        instance.delete()

        serializer = ProductSerializer(
            all_objects(Product.objects, model_name="Product"),
            context={'request': request},
            many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(responses=ProductSerializer)
    @action(
        methods=['get'],
        detail=False,
        url_path=r"(?P<product_id>[^/]+)",
        url_name="product_by_id"
    )
    def product_by_id(self, request, product_id=None):
        """
        An endpoint to return single product by `product_id`
        """
        serializer = ProductSerializer(
            get_object(
                all_objects(Product.objects, model_name="Product"),
                context={'request': request},
                fields={
                    'product_id': product_id,
                },
                model_name='Product'
            ),
            many=False
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductImageViewSet(viewsets.ViewSet):
    """
    Viewset for ProductImage
    """
    queryset = all_objects(ProductImage.objects, model_name="ProductImage")

    def __fix_image_order(self, product_id):
        logger.info("__fix_image_order: started")

        images = filter_objects(
            all_objects(ProductImage.objects, model_name="ProductImage"),
            fields={
                'product__product_id': product_id,
            },
            model_name='ProductImage'
        )
        sorted_images = sorted(images, key=lambda x: x.image_order)

        with transaction.atomic():
            for order, image in enumerate(sorted_images, start=1):
                image.image_order = order
                image.save()

        logger.info("__fix_image_order: ended")

        try:
            logger.info('updaing product profile_image')
            image = get_object(
                ProductImage.objects,
                fields={'product__product_id': product_id, 'image_order': 1},
                model_name="ProductImage"
            )
            product = get_object(
                Product.objects,
                fields={'product_id': product_id, },
                model_name="Product"
            )
            product.profile_image = image.image
            product.save()

            logger.info('product profile_image update completed')
        except Exception as e:
            logger.info("product profile_image update exception: ", e)

    def __update_image_order(self, order, product_id):
        images = filter_objects(
            all_objects(ProductImage.objects, model_name="ProductImage"),
            fields={
                'product__product_id': product_id,
            },
            model_name='ProductImage'
        )
        with transaction.atomic():
            for image in images:
                image.image_order = order[image.image_id]
                image.save()

        image = get_object(
            ProductImage.objects,
            fields={'product__product_id': product_id, 'image_order': 1},
            model_name="ProductImage"
        )
        product = get_object(
            Product.objects,
            fields={'product_id': product_id, },
            model_name="Product"
        )
        product.profile_image = image.image
        product.save()

    @extend_schema(responses=ProductImageSerializer)
    @action(
        methods=['get'],
        detail=False,
        url_path=r"product/(?P<product_id>[^/]+)",
        url_name="product_image_list"
    )
    def product_image_list(self, request, product_id=None):
        """
        An endpoint to return products images by product
        """
        serializer = ProductImageSerializer(
            filter_objects(
                all_objects(ProductImage.objects, model_name="ProductImage"),
                fields={
                    'product__product_id': product_id,
                },
                model_name='ProductImage'
            ),
            many=True
        )
        return Response(serializer.data)

    @extend_schema(responses=ProductImageSerializer)
    @permission_classes([permissions.IsAuthenticated, permissions.IsAdminUser])
    def create(self, request):
        """An endpoint to create or update a image"""
        if not authenticate(username=request.user.username, password=request.data.get('admin_password', '')):
            return Response({'message': 'Admin Password Required'}, status=status.HTTP_401_UNAUTHORIZED)

        request_data = request.data.copy()
        request_data['image_order'] = 1000

        serializer = ProductImageSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            self.__fix_image_order(request.data.get('product'))
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_204_NO_CONTENT)

    @extend_schema(responses=ProductImageSerializer)
    @permission_classes([permissions.IsAuthenticated, permissions.IsAdminUser])
    @action(detail=False, methods=['post'], url_path="delete", url_name="delete_image")
    def delete_image(self, request):
        """Delete a image"""
        if not authenticate(username=request.user.username, password=request.data.get('admin_password', '')):
            return Response({'message': 'Admin Password Required'}, status=status.HTTP_401_UNAUTHORIZED)

        instance = get_object(
            ProductImage.objects,
            fields={'image_id': request.data.get('image_id'), },
            model_name="ProductImage"
        )
        instance.delete()
        self.__fix_image_order(request.data.get('product'))
        return Response({'status': 'OK'}, status=status.HTTP_200_OK)

    @extend_schema(responses=ProductImageSerializer)
    @permission_classes([permissions.IsAuthenticated, permissions.IsAdminUser])
    @action(detail=False, methods=['post'], url_path="update-order", url_name="update_image_order")
    def update_image_order(self, request):
        """Update the order of product images"""
        if not authenticate(username=request.user.username, password=request.data.get('admin_password', '')):
            return Response({'message': 'Admin Password Required'}, status=status.HTTP_401_UNAUTHORIZED)

        self.__update_image_order(request.data.get(
            'order'), request.data.get('product'))
        return Response({'status': 'OK'}, status=status.HTTP_200_OK)


class ProductTagViewSet(viewsets.ViewSet):
    """
    Viewset for ProductTag
    """
    queryset = all_objects(ProductTag.objects,
                           model_name="ProductTag")

    @extend_schema(responses=ProductTagSerializer)
    @action(
        methods=['get'],
        detail=False,
        url_path=r"product/(?P<product_id>[^/]+)",
        url_name="product_tag_list"
    )
    def product_tag_list(self, request, product_id=None):
        """
        An endpoint to return products images by product
        """
        serializer = ProductTagSerializer(
            filter_objects(
                all_objects(ProductTag.objects, model_name="ProductTag"),
                fields={
                    'product__product_id': product_id,
                },
                model_name='ProductTag'
            ),
            many=True
        )
        return Response(serializer.data)

    @extend_schema(responses=ProductTagSerializer)
    @permission_classes([permissions.IsAuthenticated, permissions.IsAdminUser])
    def create(self, request):
        """An endpoint to create or update a image"""
        if not authenticate(username=request.user.username, password=request.data.get('admin_password', '')):
            return Response({'message': 'Admin Password Required'}, status=status.HTTP_401_UNAUTHORIZED)

        tag, created = Tag.objects.get_or_create(
            name=request.data.get('tag', ''))
        product = get_object(
            Product.objects,
            fields={'product_id': request.data.get('product', ''), },
            model_name="Product"
        )

        logger.info(f"tag: {tag}")
        logger.info(f"product: {product}")

        product_tag = ProductTag.objects.get_or_create(
            tag=tag, product=product)

        return Response({'status': 'OK'}, status=status.HTTP_200_OK)

    @extend_schema(responses=ProductTagSerializer)
    @permission_classes([permissions.IsAuthenticated, permissions.IsAdminUser])
    @action(detail=False, methods=['post'], url_path="delete", url_name="delete_tag")
    def delete_image(self, request):
        """Delete a image"""
        if not authenticate(username=request.user.username, password=request.data.get('admin_password', '')):
            return Response({'message': 'Admin Password Required'}, status=status.HTTP_401_UNAUTHORIZED)

        instance = get_object(
            ProductTag.objects,
            fields={'tag__name': request.data.get(
                'tag'), 'product__product_id': request.data.get('product')},
            model_name="ProductTag"
        )
        instance.delete()
        return Response({'status': 'OK'}, status=status.HTTP_200_OK)


class CartProductViewSet(viewsets.ViewSet):
    """
    Viewset for CartProduct
    """
    queryset = all_objects(CartProduct.objects,
                           model_name="CartProduct")

    @extend_schema(responses=CartProductSerializer)
    @permission_classes([permissions.IsAuthenticated])
    def list(self, request):
        """
        An endpoint to retrieve items in the user's cart
        """
        cart_products = filter_objects(
            CartProduct.objects,
            fields={
                'user': request.user,
            },
            model_name='CartProduct'
        )
        serializer = CartProductSerializer(
            cart_products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(responses=CartProductSerializer)
    @permission_classes([permissions.IsAuthenticated])
    @action(
        methods=['get'],
        detail=False,
        url_path=r"update/(?P<product_id>[^/]+)/(?P<size>[^/]+)/(?P<count>[^/]+)",
        url_name="update_cart_product"
    )
    def update_cart_product(self, request, product_id, size, count):
        """
        An endpoint to update items in the user's cart
        """
        try:
            product = get_object(
                Product.objects,
                fields={
                    'product_id': product_id,
                },
                model_name='Product'
            )
            cart_item, created = CartProduct.objects.get_or_create(
                user=request.user, product=product, size=size)
            cart_item.count = int(count)
            cart_item.save()

        except Exception as e:
            print("\nexception:", e)

        return Response({'status': 'OK'}, status=status.HTTP_200_OK)

    @extend_schema(responses=CartProductSerializer)
    @permission_classes([permissions.IsAuthenticated])
    @action(
        methods=['get'],
        detail=False,
        url_path=r"delete/(?P<product_id>[^/]+)/(?P<size>[^/]+)",
        url_name="delete_cart_product"
    )
    def delete_cart_product(self, request, product_id, size):
        """
        An endpoint to delete item from the user's cart
        """
        product = get_object(
            Product.objects,
            fields={
                'product_id': product_id,
            },
            model_name='Product'
        )
        cart_product = get_object(
            CartProduct.objects,
            fields={
                'product': product,
                'user': request.user,
                'size': size,
            },
            model_name='CartProduct'
        )
        cart_product.delete()

        return Response({'status': 'OK'}, status=status.HTTP_200_OK)

    @extend_schema(responses=CartProductSerializer)
    @permission_classes([permissions.IsAuthenticated])
    @action(
        methods=['post'],
        detail=False,
        url_path="batch-add",
        url_name="batch_add_to_cart"
    )
    def batch_add_to_cart(self, request):
        """
        An endpoint to batch add items in the user's cart : recive a list of (product_id, size, count) by `cart` key.
        """
        cart_item_list = request.data.get('cart', [])
        print("\ncart_item_list:", cart_item_list)

        cnt = 0
        for item in cart_item_list:
            try:
                product = get_object(
                    Product.objects,
                    fields={
                        'product_id': item['product']['product_id'],
                    },
                    model_name='Product'
                )
                cart_item, created = CartProduct.objects.get_or_create(
                    user=request.user, product=product, size=item['size'])
                cart_item.count = int(item['count'])
                cart_item.save()
                if created:
                    cnt += 1
            except Exception as e:
                print("Exception:", e)

        if cnt > 0:
            return Response({'status': 'OK', 'created': cnt}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'FAILED', }, status=status.HTTP_204_NO_CONTENT)

    @extend_schema(responses=CartProductSerializer)
    @permission_classes([permissions.IsAuthenticated])
    @action(
        methods=['get'],
        detail=False,
        url_path="revalidate",
        url_name="revalidate_cart"
    )
    def revalidate_cart(self, request):
        """
        An endpoint to revalidate the user's cart according to stock
        """

        cart_items = filter_objects(
            CartProduct.objects,
            fields={
                'user': request.user,
            },
            model_name='CartProduct'
        )

        is_updated = False
        is_deleted = False

        for item in cart_items:
            stock = ProductStock.objects.filter(
                product=item.product, size=item.size)
            current_stock = stock[0].count if len(stock) > 0 else 0

            logger.info(
                f"in cart: {item.count} | current_stock: {current_stock}")

            if item.count > current_stock:
                item.count = current_stock
                item.save()
                is_updated = True

            if item.count == 0:
                product = Product.objects.get(
                    product_id=item.product.product_id)
                wishlist_item, created = WishListProduct.objects.get_or_create(
                    user=request.user, product=product)
                item.delete()
                is_deleted = True

        return Response({'is_updated': is_updated, 'is_deleted': is_deleted}, status=status.HTTP_200_OK)


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
            WishListProduct.objects,
            fields={
                'user': request.user,
            },
            model_name='WishListProduct'
        )
        serializer = WishListProductSerializer(
            wishlist_products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(responses=WishListProductSerializer)
    @permission_classes([permissions.IsAuthenticated])
    @action(
        methods=['get'],
        detail=False,
        url_path=r"add/(?P<product_id>[^/]+)",
        url_name="add_wishlist_product"
    )
    def add_wishlist_product(self, request, product_id):
        """
        An endpoint to add items in the user's wishlist
        """
        try:
            WishListProduct.objects.create(
                user=request.user, product__product_id=product_id)

        except Exception as e:
            print("\nexception:", e)

        return Response({'status': 'OK'}, status=status.HTTP_200_OK)

    @extend_schema(responses=WishListProductSerializer)
    @permission_classes([permissions.IsAuthenticated])
    @action(
        methods=['get'],
        detail=False,
        url_path=r"delete/(?P<product_id>[^/]+)",
        url_name="delete_wishlist_product"
    )
    def delete_wishlist_product(self, request, product_id):
        """
        An endpoint to delete item from the user's wishlist
        """
        wishlist_product = get_object(
            WishListProduct.objects,
            fields={
                'product__product_id': product_id,
                'user': request.user
            },
            model_name='WishListProduct'
        )
        wishlist_product.delete()

        return Response({'status': 'OK'}, status=status.HTTP_200_OK)

    @extend_schema(responses=WishListProductSerializer)
    @permission_classes([permissions.IsAuthenticated])
    @action(
        methods=['post'],
        detail=False,
        url_path="batch-add",
        url_name="batch_add_to_wishlist"
    )
    def batch_add_to_wishlist(self, request):
        """
        An endpoint to batch add items in the user's wishlist : recive a list of product_id with `wishlist` key.
        """
        products_list = request.data.get('wishlist', [])
        print("\nproducts_list:", products_list)

        cnt = 0
        for product_id in products_list:
            try:
                product = Product.objects.get(product_id=product_id)
                wishlist_item, created = WishListProduct.objects.get_or_create(
                    user=request.user, product=product)
                if created:
                    cnt += 1
            except Product.DoesNotExist:
                print(
                    f"Product with product_id '{product_id}' does not exist.")
            except Exception as e:
                print("Exception:", e)

        if cnt > 0:
            return Response({'status': 'OK', 'created': cnt}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'FAILED', }, status=status.HTTP_204_NO_CONTENT)
