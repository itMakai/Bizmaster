from datetime import timezone
from django.utils import timezone
from django.db import models
from django.utils import timezone

from django.utils.text import slugify
from django.contrib.auth.models import User

# Create your models here.


class Customer(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/images')
    
    def __str__(self):
        return f'{self.first_name}'
    
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)   
    order_date = models.DateField(default=timezone.now)
    paid = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.customer} | {self.order_date}'
    
    


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=9)
    in_stock = models.IntegerField()
    description = models.TextField(blank=True, null=True)

    available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(upload_to='media/images')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name} ({self.price})'
    

class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    amount = models.DecimalField(decimal_places=2, max_digits=9)
    
    def __str__(self):
        return f'{self.order} | {self.product} | {self.quantity}'
    
    
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
