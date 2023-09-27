from django.shortcuts import render, redirect
from ..models import Product, Cart, ShippingFee, Customer
from django.views import View
from django.contrib import messages
from django.http.response import JsonResponse
from ..validators.cart_validators.add_to_cart_validator import validate_quantity, validate_size_color
from ..validators.cart_validators.cart_view_validator import validate_quantity_list, validate_total_price

class CartView(View):
     def get(self, request):
        if not request.user.is_authenticated:
            return redirect("login")
        return render(request, "app/cart.html")
     def post(self, request):
        listQuantity = [request.POST.get('quantityItem' + item) for item in request.POST.getlist('itemCart')]
        listItem = request.POST.getlist('itemCart');
        totalPrice = request.POST.get('totalPrice')
        listPrice = [request.POST.get('price' + item) for item in request.POST.getlist('itemCart')]
        if not validate_total_price(request, totalPrice) or not validate_quantity_list(request, listQuantity):
            return render(request, "app/cart.html")
        
        cart = request.session.get('cart', {})
        cart['listItem'] = listItem
        cart['listQuantity'] = listQuantity
        cart['totalPrice'] = totalPrice
        cart['listPrice'] = listPrice
        request.session['cart'] = cart        
        return redirect("checkout")
     
class AddToCartView(View):
    def post(self, request):
        if request.user.is_authenticated:
            size  = request.POST.get('size')
            color = request.POST.get('color')
            quantity = request.POST.get('quantity')
            if request.POST.get('quantity'):
                quantity = int(request.POST.get('quantity'))
            product = Product.objects.get(id=request.POST.get('product_id'))
            quantity_error = validate_quantity(quantity)
            size_color_error = validate_size_color(size, color)
            if quantity_error:
                return quantity_error
            if size_color_error:
                return size_color_error
            cart = Cart.objects.filter(user = request.user, product= product, size=size, color=color)
            if cart.exists():
                cart = cart.first()
                cart.quantity += quantity
                cart.save()
            else:
                Cart.objects.create(user=request.user, product= product, quantity=quantity, size=size, color=color)
            return JsonResponse({'message': "Sản phẩm đã được thêm vào giỏ hàng"}, status=200)
        else:
            return JsonResponse({'error': "Not Login"}, status=403)
        
class RemoveFromCartView(View):
    def post(self, request):
        if request.user.is_authenticated:
            cart_item_id = request.POST.get('cart_item_id')
            try:
                cart_item = Cart.objects.get(id=cart_item_id, user=request.user)
                cart_item.delete()
                cart = request.session.get('cart', {})
                if cart_item.id in cart.get('listItem', []):
                    index = cart['listItem'].index(cart_item.id)
                    del cart['listItem'][index]
                    del cart['listQuantity'][index]
                    del cart['listPrice'][index]
                    cart['totalPrice'] -= cart_item.product.price * cart_item.quantity
                    request.session['cart'] = cart
                return JsonResponse({'success': True, 'message': 'Item removed from the cart'}, status=200)
            except Cart.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Cart item not found'}, status=404)
        else:
            return JsonResponse({'success': False, 'error': 'Not authenticated'}, status=403)