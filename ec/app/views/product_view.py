from django.shortcuts import render
from ..models import Product, Skus, Attributes
from django.views import View

class ProductDetail(View):
    def get(self, request, pk):
        product = Product.objects.get(id=pk)
        skus_with_units = Skus.objects.filter(product=product, unit_amount__gt=0)
        attributes = Attributes.objects.filter(skus__in=skus_with_units)
        attribute_size = attributes.values_list('size', flat=True).distinct()
        attribute_color = attributes.values_list('color', flat=True).distinct()   
        context = {'product': product, 
                   'attribute_size' : attribute_size,
                   'attribute_color' : attribute_color,
                   'title' : 'SHOP DETAILS',
                   }
        return render(request, "app/detail.html", context)
