from django.db import models
from django.contrib.auth.models import User
from sales.models import Product, Customer, Category

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image_url = models.URLField(max_length=200, default='https://via.placeholder.com/100')
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    image = models.ImageField(upload_to='media/images')

    def __str__(self):
        return self.user.username

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"Favorite {self.product_name} by {self.user.username}"
