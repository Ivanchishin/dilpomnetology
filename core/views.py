from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import authenticate, login

from .importyaml import import_shop_from_yaml
from .models import ProductInfo, Basket, BasketItem, Order, OrderItem, Address
from .serializers import *
from .services import send_order_emails


#Авторизация

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
            return Response({"error": "Invalid credentials"}, status=400)

        login(request, user)
        return Response({"status": "logged in"})


#Товары

class ProductViewSet(ModelViewSet):
    queryset = ProductInfo.objects.all()
    serializer_class = ProductInfoSerializer
    permission_classes = [AllowAny]


#Адреса

class AddressViewSet(ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Только адреса текущего пользователя
        return Address.objects.filter(
            user=self.request.user
        )
    def perform_create(self, serializer):
        # Автоматическая привязка адреса
        serializer.save(user=self.request.user)

    def perform_create(self, serializer):
        # Адрес автоматически привязывается к пользователю
        serializer.save(user=self.request.user)


#Корзина

class BasketView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        basket, _ = Basket.objects.get_or_create(
            user=request.user
        )
        serializer = BasketSerializer(basket)
        return Response(serializer.data)


class BasketAddView(GenericAPIView):
    serializer_class = BasketAddSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        basket, _ = Basket.objects.get_or_create(user=request.user)

        item, created = BasketItem.objects.get_or_create(
            basket=basket,
            product_info_id=serializer.validated_data['product_info_id'],
            defaults={'quantity': serializer.validated_data['quantity']}
        )

        if not created:
            item.quantity += serializer.validated_data['quantity']
            item.save()

        return Response({"status": "added"})


class BasketRemoveView(GenericAPIView):
    serializer_class = BasketRemoveSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        BasketItem.objects.filter(
            id=serializer.validated_data['item_id'],
            basket__user=request.user
        ).delete()

        return Response({"status": "removed"})


#Заказ

class OrderCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        basket = Basket.objects.get(user=request.user)

        if not basket.items.exists():
            return Response(
                {"error": "Basket is empty"},
                status=400
            )

        order = Order.objects.create(user=request.user)

        for item in basket.items.all():
            OrderItem.objects.create(
                order=order,
                product_info=item.product_info,
                quantity=item.quantity
            )
        send_order_emails(order)
        basket.items.all().delete()
        return Response({
            "status": "заказ создан",
            "order_id": order.id
        })


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Только заказы текущего пользователя
        return Order.objects.filter(
            user=self.request.user
        ).exclude(
            status='basket'
        )

@method_decorator(csrf_exempt, name='dispatch')
class ImportShopView(GenericAPIView):
    serializer_class = ImportSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        file = serializer.validated_data['file']

        try:
            import_shop_from_yaml(file, request.user)
        except Exception as e:
            return Response({"error": str(e)}, status=400)

        return Response({"status": "import completed"})




class ConfirmOrderView(GenericAPIView):
    serializer_class = ConfirmOrderSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        address = Address.objects.filter(
            id=serializer.validated_data['address_id'],
            user=request.user
        ).first()

        if not address:
            return Response(
                {"error": "Address not found"},
                status=404
            )

        basket = Basket.objects.get(user=request.user)

        if not basket.items.exists():
            return Response(
                {"error": "Basket is empty"},
                status=400
            )

        order = Order.objects.create(
            user=request.user,
            address=address,
            status='pending'
        )

        for item in basket.items.all():
            OrderItem.objects.create(
                order=order,
                product_info=item.product_info,
                quantity=item.quantity
            )

        send_order_emails(order)
        basket.items.all().delete()

        return Response({
            "status": "order confirmed",
            "order_id": order.id
        })