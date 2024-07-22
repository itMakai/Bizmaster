from django.contrib import admin
from sales.models import Category, Product, Customer, Order, OrderDetail

# Register your models here.
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderDetail)
admin.site.register(Category)