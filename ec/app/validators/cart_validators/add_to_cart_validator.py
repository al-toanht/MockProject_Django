from django.http import JsonResponse

def validate_quantity(quantity):
    if not quantity or quantity <= 0:
        return JsonResponse({'error': "Số lượng không hợp lệ"}, status=400)
    return None

def validate_size_color(size, color):
    if size is None or color is None:
        return JsonResponse({'error': "Vui lòng phân loại hàng"}, status=403)
    return None