from django.shortcuts import render, redirect
from ..models import Product, Cart, ShippingFee, Customer, Order, OrderItem, Payment
from django.views import View
from ..constants import PaymentStatus, OrderStatus
from django.http.response import JsonResponse
from ..validators.order_validators.add_order_validator import validates
class CheckoutView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("login")
        if request.session.get('cart') is not None:
            user_email = request.user.email if hasattr(request.user, 'email') else None 
            cart = request.session.get('cart', {})  
            listItem = cart.get('listItem', [])          

            cart_products  = Cart.objects.filter(id__in=listItem)
            product_ids = cart_products.values_list('product_id', flat=True)
            products_info = Product.objects.filter(id__in=product_ids)
            shippingFee = ShippingFee.objects.all()

            customer = Customer.objects.filter(user=request.user).first()
        else:
            return redirect("cart")
        return render(request, "app/checkout.html", {
            'cart': cart,
            'cart_products': cart_products,
            'products_info': products_info, 
            'shippingFee': shippingFee,
            'customer': customer,
            'user_email' : user_email
        })
     
    def post(self, request):
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        shipping_address = request.POST.get('shipping_address')
        city = request.POST.get('city')
        total_price = request.POST.get('totalPrice')
        payment_method = request.POST.get('payment_method')
        list_productId = request.POST.getlist('productId')
        list_quantity = request.POST.getlist('quantity')
        list_price = request.POST.getlist('price')
        error_messages = validates(email, phone_number, shipping_address, payment_method)
        if error_messages:
            return JsonResponse({'errors': error_messages}, status=400)
        else:
            order = Order.objects.create(
                user=request.user,
                status=OrderStatus.PENDING,
                shipping_address=shipping_address,
                city=city,
                email=email,
                phone_number=phone_number,
                total_price=total_price
            )
            if order.id is not None:
                for product_id, quantity, price in zip(list_productId, list_quantity, list_price):
                    print('product_id' + product_id)
                    product = Product.objects.get(pk=product_id)
                    OrderItem.objects.create(order=order, product=product, quantity=quantity, price=price)

                Payment.objects.create(
                    payment_status= PaymentStatus.PENDING,
                    order = order,
                    payment_amount = 0,
                    payment_method = payment_method
                )

                # Xóa session 'cart' sau khi xử lý xong đơn hàng
                if 'cart' in request.session:
                    cart = request.session.get('cart', {})  
                    listItem = cart.get('listItem', [])          
                    Cart.objects.filter(id__in=listItem).delete()
                    del request.session['cart']
                
                return JsonResponse({'message': "Đơn hàng đã được thêm thành công"}, status=200)
     
        