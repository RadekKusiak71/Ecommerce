from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.utils import timezone

class Profile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=9,null=True)

    def __str__(self):
        return f'{self.firstname} {self.lastname}'
    
class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    description = models.TextField(null=True)
    name = models.CharField(max_length=100)
    product_number = models.CharField(max_length=7)
    price = models.FloatField()
    quantity = models.IntegerField()
    image = models.ImageField(upload_to='main/static/product_images',null=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        if self.is_available:
            return f'{self.name} is available'
        else:
            return f'{self.name} is unavailable'
    
    def availability(self):
        if self.quantity != 0:
            self.is_available = True
        else:
            self.is_available = False
        self.save()

class Cart(models.Model):
    owner = models.ForeignKey(Profile,on_delete=models.CASCADE,null=True)
    session_key = models.CharField(max_length=255,null=True)

    def __str__(self):
        if self.owner:
            return f'Cart for {self.owner.firstname} {self.owner.lastname}'
        else:
            return f'Cart for {self.session_key}'
        
class CartItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=1)

    def __str__(self):
        return f'Item {self.product.name} - {self.quantity} for cart {self.cart.id}'
    
class Order(models.Model):
    owner = models.ForeignKey(Profile,on_delete=models.CASCADE,null=True)
    session_key = models.CharField(max_length=255,null=True)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        if self.owner:
            return f'Order for {self.owner.firstname} {self.owner.lastname}'
        else:
            return f'Order for {self.session_key}'
        
class OrderItem(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=1)

    def __str__(self):
        if self.order.owner:
            return f"{self.order.owner} - {self.product.name}"
        else:
            return f"{self.order.session_key} - {self.product.name}"
        
class OrderDetails(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=9)
    address = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=timezone.now)
    status = models.BooleanField(default=False)
    order = models.ForeignKey('Order',on_delete=models.CASCADE,null=True)
    total_price = models.FloatField(default=0)

    def __str__(self):
        if self.status:
            return f'Order for {self.first_name} {self.last_name} - status: Not Ready to send'
        else:
            return f'Order for {self.first_name} {self.last_name} - status: Ready to send'