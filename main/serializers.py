from rest_framework import serializers
from .models import Product,Category,Order,Profile,OrderItem
from django.contrib.auth.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ('phone_number', 'email')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name','last_name')

class OrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"