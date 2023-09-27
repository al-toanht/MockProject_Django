from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from PIL import Image
from django.contrib.auth.models import User 
# Create your models here.

class Category(MPTTModel):
    name = models.CharField(max_length=200)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by=['name']
    def __str__(self):                           
       return self.name
    
class Product(models.Model):
    title = models.CharField(max_length=100)
    short_description = models.CharField(max_length=255)
    long_description = models.TextField(null=True, blank=True)
    selling_price = models.FloatField()
    discount_price = models.FloatField(null=True, blank=True)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    product_image = models.ImageField(upload_to='product', 
        null=True,
        blank=True,
        editable=True,
        help_text="Profile Picture",
        verbose_name="Profile Picture")
    def __str__(self):
        return self.title
    def save(self):
        if not self.product_image:
            return            
        super(Product, self).save()
        image = Image.open(self.product_image)
        size = ( 419, 419)
        image = image.resize(size, Image.ANTIALIAS)
        image.save(self.product_image.path)

class Skus(models.Model):
    sku = models.CharField(max_length=255, unique=True)
    unit_amount = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='models_sku', related_query_name='model_sku')
    def __str__(self):
        return self.sku
    
class Attributes(models.Model):
    skus = models.OneToOneField(Skus, on_delete=models.CASCADE, related_name='models_sku', related_query_name='model_sku')
    size = models.CharField(max_length=10)
    color = models.CharField(max_length=50)
    def __str__(self):
        return self.skus.sku + ' ' + self.size +  ' ' + self.color

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    mobile = models.CharField(max_length=20)
    def __str__(self):
        return self.name

class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='models_cart', related_query_name='model_cart')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=1)
    size = models.CharField(max_length=10)
    color = models.CharField(max_length=50)

    @property
    def total_cost(self):
        return self.quantity * self.product.discount_price
    
class Order(models.Model):
    ORDER_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=ORDER_STATUS_CHOICES)
    shipping_address = models.TextField()
    city = models.CharField(max_length=50)
    email = models.EmailField(default='example@example.com')
    phone_number = models.CharField(max_length=15, default='N/A')  # Thêm trường số điện thoại
    total_price = models.DecimalField(max_digits=10, decimal_places=2) # Tổng giá trị của đơn hàng

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Giá tiền của từng sản phẩm

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )
    payment_status = models.CharField(max_length=50, choices=PAYMENT_STATUS_CHOICES)
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=100, null=True)
        
    def __str__(self):
        return f"Payment for Order #{self.order.pk}"
    
class ShippingFee(models.Model):
    region = models.CharField(max_length=100) 
    postal_code = models.CharField(max_length=20) 
    fee = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.region

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)  # Mã coupon
    discount_type = models.CharField(max_length=10)  # Loại giảm giá (percentage hoặc fixed)
    value = models.DecimalField(max_digits=10, decimal_places=2)  # Giá trị giảm giá
    expiry_date = models.DateField()  # Thời hạn sử dụng
    max_usage = models.PositiveIntegerField()  # Số lần sử dụng tối đa
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code