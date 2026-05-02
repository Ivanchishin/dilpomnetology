from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# ===================== USERS =====================

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        user = self.model(email=email)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


# ===================== SUPPLIERS =====================

class Supplier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)


# ===================== PRODUCTS =====================

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()


class ProductInfo(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()


class Parameter(models.Model):
    name = models.CharField(max_length=255)


class ProductParameter(models.Model):
    product_info = models.ForeignKey(ProductInfo, on_delete=models.CASCADE)
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)


# ===================== CONTACTS =====================

class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)


# ===================== ORDERS =====================

class Order(models.Model):
    STATUS = (
        ('basket', 'Basket'),
        ('new', 'New'),
        ('confirmed', 'Confirmed'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact, null=True, blank=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=20, choices=STATUS, default='basket')
    created_at = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_info = models.ForeignKey(ProductInfo, on_delete=models.CASCADE)
    quantity = models.IntegerField()