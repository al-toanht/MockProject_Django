from django.shortcuts import render
from ..models import Product, Category
from django.views import View
from django.db.models import Sum

class CategoryView(View):
    def get(self, request, val):
        products = Product.objects.filter(category=val).annotate(total_unit=Sum('model_sku__unit_amount')).exclude(total_unit=0)
        category_name = Category.objects.get(id=val)
        context = {'products': products,
                   'title' : category_name,
                    }
        return render(request, "app/shop.html", context)