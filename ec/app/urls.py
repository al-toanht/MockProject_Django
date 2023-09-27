from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views.auth_views import LogOutView, CustomerLoginView, CustomerRegisterView
from .views.home_view import HomeView
from .views.product_view import ProductDetail
from .views.profile_view import CustomerProfileView
from .views.category_view import CategoryView
from .views.cart_view import CartView, AddToCartView, RemoveFromCartView
from .views.checkout_views import CheckoutView


urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("login", CustomerLoginView.as_view(), name="login"),
    path("register", CustomerRegisterView.as_view(), name="register"),
    path("profile", CustomerProfileView.as_view(), name="profile"),
    path("logout", LogOutView.as_view(), name='logout'),
    path("category/<int:val>", CategoryView.as_view(), name="category"),
    path("product-detail/<int:pk>", ProductDetail.as_view(), name="product-detail"),
    path("add-to-cart", AddToCartView.as_view(), name='add-to-cart'),
    path('remove-from-cart/', RemoveFromCartView.as_view(), name='remove_from_cart'),
    path("cart", CartView.as_view(), name='cart'),
    path("check-out", CheckoutView.as_view(), name='checkout'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
