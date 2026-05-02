from django.urls import path, include
from rest_framework.routers import DefaultRouter
import core.views as views
from django.contrib import admin

router = DefaultRouter()
router.register('products', views.ProductViewSet)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.RegisterView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('basket/', views.BasketView.as_view()),
    path('order/confirm/', views.ConfirmOrderView.as_view()),
    path('import/', views.ImportShopView.as_view()),
    path('', include(router.urls)),
]