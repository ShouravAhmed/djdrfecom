from rest_framework import serializers

from .models import (CartProduct, Product, ProductCategory, ProductDescription,
                     ProductPhoto, ProductSizeChart, ProductTag, Store, Tag,
                     WishListProduct)


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = "__all__"


class ProductDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDescription
        fields = "__all__"


class ProductSizeChartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSizeChart
        fields = "__all__"


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['id', 'store_name', 'contact_number', 'address']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ['product_buy_price']


class ProductPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPhoto
        fields = "__all__"


class ProductTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTag
        fields = "__all__"


class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartProduct
        fields = "__all__"


class WishListProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishListProduct
        fields = "__all__"
