from . models import Product, Category, Skus, Customer, Attributes, Cart

def cart_context(request):
    if request.user.is_authenticated:
        cart_context = Cart.objects.filter(user = request.user)
    else:
        cart_context = None
    
    return {'cart_context': cart_context}

def category_context(request):
    return {'categories': Category.objects.filter(parent=None)}