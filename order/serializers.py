from django.db.models import Q
from rest_framework import serializers

from product.serializers import ProductSerializer

from .models import Order, OrderedProduct, OrderNote, Review


class OrderedProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderedProduct
        fields = '__all__'


class OrderNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderNote
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    courier_choice = serializers.CharField(source='get_courier_choice_display')
    delivery_type = serializers.CharField(source='get_delivery_type_display')
    item_type = serializers.CharField(source='get_item_type_display')
    payment_method = serializers.CharField(source='get_payment_method_display')
    order_status = serializers.CharField(source='get_order_status_display')
    payment_status = serializers.CharField(source='get_payment_status_display')

    ordered_products = OrderedProductSerializer(
        many=True, read_only=True, source='orderedproduct_set')

    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(OrderSerializer, self).__init__(*args, **kwargs)
        is_admin = self.context['request'].user.is_staff if 'request' in self.context else False

        if not is_admin:
            self.fields.pop('products_base_value')
            self.fields.pop('order_profit')
        else:
            self.fields['order_notes'] = OrderNoteSerializer(
                many=True, read_only=True, source='ordernote_set')

    def get_reviews(self, obj):
        user = self.context['request'].user if 'request' in self.context else None

        if user and user.is_staff:
            reviews = obj.review_set.all()
        else:
            reviews = obj.review_set.filter(
                Q(is_approved=True) | Q(order__customer=user)
            )

        return ReviewSerializer(reviews, many=True, context=self.context).data

    def to_representation(self, instance):
        # Get the base representation
        representation = super(
            OrderSerializer, self).to_representation(instance)

        # Format the created_at field
        if 'created_at' in representation:
            created_at = instance.created_at
            representation['created_at'] = created_at.strftime(
                '%B %d, %Y %I.%M %p')

        return representation
