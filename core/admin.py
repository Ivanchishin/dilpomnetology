from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model

from .models import *

User = get_user_model()



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description']

@admin.register(Parameter)
class ParameterAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'city', 'street', 'house', 'building','structure','apartment']



@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ['email']   # ← ВАЖНО

    list_display = ['id', 'email', 'first_name', 'last_name', 'is_staff']
    search_fields = ['email', 'first_name', 'last_name']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'middle_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'is_active']


class ProductParameterInline(admin.TabularInline):
    model = ProductParameter
    extra = 1


@admin.register(ProductInfo)
class ProductInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'supplier', 'price', 'quantity']
    inlines = [ProductParameterInline]


class BasketItemInline(admin.TabularInline):
    model = BasketItem
    extra = 0

    readonly_fields = ['product_name', 'supplier_name', 'item_total']

    fields = [
        'product_name',
        'supplier_name',
        'quantity',
        'item_total'
    ]

    def product_name(self, obj):
        return obj.product_info.product.name

    def supplier_name(self, obj):
        return obj.product_info.supplier.name

    def item_total(self, obj):
        return obj.total_price()


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'basket_total']
    inlines = [BasketItemInline]

    def basket_total(self, obj):
        return obj.total_sum()


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'created_at', 'order_total']
    inlines = [OrderItemInline]

    def order_total(self, obj):
        return obj.total_sum()