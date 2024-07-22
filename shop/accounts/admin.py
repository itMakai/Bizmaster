from django.contrib import admin
from .models import Profile, Order, Favorite

# Register your models here.
admin.site.register(Profile)
admin.site.register(Order)
admin.site.register(Favorite)
# Compare this snippet from shop/sales/views.py:
