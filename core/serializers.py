from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import (
    Supplier,
    Product,
    ProductInfo,
    Parameter,
    ProductParameter,
    Address,
    Basket,
    BasketItem,
    Order,
    OrderItem,
)

User = get_user_model()

class ConfirmOrderSerializer(serializers.Serializer):
    address_id = serializers.IntegerField()

class ImportSerializer(serializers.Serializer):
    file = serializers.FileField()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'middle_name']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()



class ProductParameterSerializer(serializers.ModelSerializer):
    parameter = serializers.StringRelatedField()

    class Meta:
        model = ProductParameter
        fields = ['parameter', 'value']


class ProductInfoSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()
    supplier = serializers.StringRelatedField()
    parameters = ProductParameterSerializer(many=True, read_only=True)

    class Meta:
        model = ProductInfo
        fields = ['id', 'product', 'supplier', 'price', 'quantity', 'parameters']



class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = [
            'id',
            'city',
            'street',
            'house',
            'building',
            'structure',
            'apartment'
        ]



class BasketItemSerializer(serializers.ModelSerializer):
    product_info = ProductInfoSerializer(read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = BasketItem
        fields = ['id', 'product_info', 'quantity', 'total_price']

    def get_total_price(self, obj):
        return obj.total_price()


class BasketSerializer(serializers.ModelSerializer):
    items = BasketItemSerializer(many=True, read_only=True)
    total_sum = serializers.SerializerMethodField()

    class Meta:
        model = Basket
        fields = ['id', 'items', 'total_sum']

    def get_total_sum(self, obj):
        return obj.total_sum()


class BasketAddSerializer(serializers.Serializer):
    product_info_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)


class BasketRemoveSerializer(serializers.Serializer):
    item_id = serializers.IntegerField()



class OrderItemSerializer(serializers.ModelSerializer):
    product_info = ProductInfoSerializer(read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['product_info', 'quantity', 'total_price']

    def get_total_price(self, obj):
        return obj.total_price()


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_sum = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'created_at', 'status', 'items', 'total_sum']

    def get_total_sum(self, obj):
        return obj.total_sum()