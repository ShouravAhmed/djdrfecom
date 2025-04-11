from rest_framework import serializers

from .models import (CartProduct, Product, ProductCategory, ProductDescription,
                     ProductImage, ProductSizeChart, ProductStock, ProductTag,
                     Store, Tag, WishListProduct)


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = "__all__"


class ProductDescriptionSerializer(serializers.ModelSerializer):
    product_category = ProductCategorySerializer

    class Meta:
        model = ProductDescription
        fields = "__all__"


class ProductSizeChartSerializer(serializers.ModelSerializer):
    product_category = ProductCategorySerializer

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
    product_category = ProductCategorySerializer()
    product_description = ProductDescriptionSerializer()
    product_size_chart = ProductSizeChartSerializer()
    store = StoreSerializer()
    product_stock = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ProductSerializer, self).__init__(*args, **kwargs)
        is_admin = self.context['request'].user.is_staff if 'request' in self.context else False
        if not is_admin:
            self.fields.pop('product_base_price')

    def get_product_stock(self, obj):
        stock_entries = ProductStock.objects.filter(product=obj)
        stock_dict = {entry.size: entry.count for entry in stock_entries}
        return stock_dict


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class ProductTagSerializer(serializers.ModelSerializer):
    tag = TagSerializer()

    class Meta:
        model = ProductTag
        fields = "__all__"


class CartProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartProduct
        fields = "__all__"


class WishListProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = WishListProduct
        fields = "__all__"
