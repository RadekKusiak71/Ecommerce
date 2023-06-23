from django.contrib import admin
from .models import Profile, Category, Product, Cart , CartItem, Order, OrderItem, Order_details

admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Order_details)
