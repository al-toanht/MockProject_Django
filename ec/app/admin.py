from django.contrib import admin
from .models import Product, Category, Skus, Customer, Attributes, Cart

# Register your models here.
admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Skus)
admin.site.register(Attributes)
admin.site.register(Cart)
