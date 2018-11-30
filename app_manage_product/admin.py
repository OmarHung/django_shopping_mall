from django.contrib import admin
from .models import Product, Product_spec

# Register your models here.
admin.site.register(Product)
admin.site.register(Product_spec)