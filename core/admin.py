from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.urls import path

from core.importyaml import import_shop_from_yaml
from .models import (
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


# ===================== USER =====================

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ['email']
    list_display = ['id', 'email', 'first_name', 'last_name', 'is_staff', 'is_active']
    search_fields = ['email', 'first_name', 'last_name']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    filter_horizontal = ('groups', 'user_permissions')


# ===================== SUPPLIER =====================

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'user', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']


# ===================== PRODUCTS =====================

class ProductParameterInline(admin.TabularInline):
    model = ProductParameter
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


@admin.register(ProductInfo)
class ProductInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'supplier', 'price', 'quantity']
    list_filter = ['supplier']
    search_fields = ['product__name']
    inlines = [ProductParameterInline]


@admin.register(Parameter)
class ParameterAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


# ===================== CONTACT =====================

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'phone', 'city', 'street']
    search_fields = ['phone', 'city']


# ===================== ORDERS =====================

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'created_at']
    list_filter = ['status']
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product_info', 'quantity']

