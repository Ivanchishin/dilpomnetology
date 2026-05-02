from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status

from django.contrib.auth import authenticate

from .models import (
    ProductInfo,
    Order,
    OrderItem,
    Contact,
)

from .serializers import (
    UserSerializer,
    ProductInfoSerializer,
    OrderItemSerializer,
    OrderSerializer,
    ContactSerializer,
    BasketAddSerializer,
    BasketRemoveSerializer,
    ConfirmOrderSerializer, LoginSerializer,
)


# ===================== AUTH =====================

class RegisterView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )

        if not user:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response({"status": "logged in"})

# ===================== PRODUCTS =====================

class ProductViewSet(ModelViewSet):
    queryset = ProductInfo.objects.all()
    serializer_class = ProductInfoSerializer
    permission_classes = [AllowAny]


# ===================== CONTACTS =====================

class ContactViewSet(ModelViewSet):
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Contact.objects.filter(user=self.request.user)


# ===================== BASKET =====================

class BasketView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        order, _ = Order.objects.get_or_create(
            user=request.user,
            status='basket'
        )

        items = OrderItem.objects.filter(order=order)
        serializer = OrderItemSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BasketAddSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order, _ = Order.objects.get_or_create(
            user=request.user,
            status='basket'
        )

        OrderItem.objects.create(
            order=order,
            product_info=serializer.validated_data['product_info'],
            quantity=serializer.validated_data['quantity']
        )

        return Response({"status": "added"})


class BasketRemoveView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = BasketRemoveSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        item = OrderItem.objects.filter(
            id=serializer.validated_data['item_id'],
            order__user=request.user,
            order__status='basket'
        ).first()

        if not item:
            return Response(
                {"error": "item not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        item.delete()
        return Response({"status": "removed"})


# ===================== ORDER =====================

class ConfirmOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ConfirmOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order = Order.objects.filter(
            id=serializer.validated_data['order_id'],
            user=request.user,
            status='basket'
        ).first()

        if not order:
            return Response(
                {"error": "order not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        order.contact = serializer.validated_data['contact_id']
        order.status = 'new'
        order.save()

        return Response({"status": "confirmed"})


# ===================== ORDERS =====================

class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).exclude(status='basket')