from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register('products', ProductViewSet)
router.register('orders', OrderViewSet)
router.register('addresses', AddressViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('import/', ImportShopView.as_view()),
    path('basket/', BasketView.as_view()),
    path('basket/add/', BasketAddView.as_view()),
    path('basket/remove/', BasketRemoveView.as_view()),
    path('order/confirm/', ConfirmOrderView.as_view()),
    path('order/create/', OrderCreateView.as_view()),

    path('', include(router.urls)),
]