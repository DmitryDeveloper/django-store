import datetime
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='images/categories', default="")

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.IntegerField(default=0)
    image = models.ImageField(upload_to='images/products', default="")

    def __str__(self):
        return self.name


class Order(models.Model):
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    building = models.CharField(max_length=50)
    flat = models.IntegerField(default=0)
    phone = models.CharField(max_length=50, default=0)
    total_price = models.CharField(max_length=50, default=0)
    ip_address = models.CharField(max_length=50, default=0)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class OrderStatus(models.TextChoices):
        PROCESSING = 'PR', _('Processing')
        DELIVERING = 'DL', _('Delivering')
        COMPLETED = 'CP', _('Completed')

    status = models.CharField(
        max_length=50,
        choices=OrderStatus.choices,
        default=OrderStatus.PROCESSING,
    )

    def __str__(self):
        return self.street


class ProductOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)

