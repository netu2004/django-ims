# inventory/models.py
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField(blank=True)
    mobile = models.CharField(max_length=15, default='0000000000')  # Or any safe default
    picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('Stationary', 'Stationary'),
        ('Electronics', 'Electronics'),
        ('Food', 'Food'),
    ]

    PRODUCT_NAME_CHOICES = [
        ('Ball Pen', 'Ball Pen'),
        ('A4 Notebook', 'A4 Notebook'),
        ('Stapler', 'Stapler'),
        ('USB Flash Drive', 'USB Flash Drive'),
        ('Wireless Mouse', 'Wireless Mouse'),
        ('Bluetooth Speaker', 'Bluetooth Speaker'),
        ('Instant Noodles', 'Instant Noodles'),
        ('Chocolate Bar', 'Chocolate Bar'),
        ('Juice Box', 'Juice Box'),
    ]

    name = models.CharField(max_length=100, choices=PRODUCT_NAME_CHOICES)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Stationary')
    quantity = models.PositiveIntegerField()
    description = models.TextField(default="Description not provided")

    def __str__(self):
        return f"{self.name} ({self.category})"




class Order(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    order_quantity = models.PositiveIntegerField(default=1)
    order_date = models.DateTimeField(default=timezone.now)

