from django.http import JsonResponse
from django.contrib import messages

def validate_total_price(request, total_price):
    if total_price == '0':
        messages.warning(request, 'Vui lòng chọn sản phẩm')
        return False
    return True

def validate_quantity_list(request, list_quantity):
    if not all(quantity != '' for quantity in list_quantity):
        messages.warning(request, 'Vui lòng chọn số lượng cho sản phẩm')
        return False
    return True