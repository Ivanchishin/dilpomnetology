from rest_framework import serializers
from django.contrib.auth import get_user_model
from core.models import (
    Supplier,
    Product,
    ProductInfo,
    Parameter,
    ProductParameter,
    Contact,
    Order,
    OrderItem,
)

User = get_user_model()


# ===================== USERS =====================

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

# ===================== SUPPLIERS =====================

class SupplierSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Supplier
        fields = '__all__'


# ===================== PRODUCTS =====================

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = '__all__'


class ProductParameterSerializer(serializers.ModelSerializer):
    parameter = serializers.PrimaryKeyRelatedField(queryset=Parameter.objects.all())

    class Meta:
        model = ProductParameter
        fields = ['parameter', 'value']


class ProductInfoSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    supplier = serializers.PrimaryKeyRelatedField(queryset=Supplier.objects.all())

    parameters = ProductParameterSerializer(
        source='productparameter_set',
        many=True,
        required=False
    )

    class Meta:
        model = ProductInfo
        fields = ['id', 'product', 'supplier', 'price', 'quantity', 'parameters']

    def create(self, validated_data):
        parameters_data = validated_data.pop('productparameter_set', [])
        product_info = ProductInfo.objects.create(**validated_data)

        for param in parameters_data:
            ProductParameter.objects.create(
                product_info=product_info,
                parameter=param['parameter'],
                value=param['value']
            )

        return product_info


# ===================== CONTACTS =====================

class ContactSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Contact
        fields = '__all__'


# ===================== ORDERS =====================

class OrderItemSerializer(serializers.ModelSerializer):
    product_info = serializers.PrimaryKeyRelatedField(
        queryset=ProductInfo.objects.all()
    )

    class Meta:
        model = OrderItem
        fields = ['id', 'product_info', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(source='orderitem_set', many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'contact', 'status', 'created_at', 'items']
        read_only_fields = ['user', 'status']


# ===================== BASKET =====================

class BasketAddSerializer(serializers.Serializer):
    product_info = serializers.PrimaryKeyRelatedField(
        queryset=ProductInfo.objects.all()
    )
    quantity = serializers.IntegerField(min_value=1)


class BasketRemoveSerializer(serializers.Serializer):
    item_id = serializers.IntegerField()


# ===================== ORDER CONFIRM =====================

class ConfirmOrderSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    contact_id = serializers.PrimaryKeyRelatedField(
        queryset=Contact.objects.all()
    )

class ImportSerializer(serializers.Serializer):
    file = serializers.FileField()