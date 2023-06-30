from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views import View
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.sessions.models import Session
from django.contrib.auth.mixins import LoginRequiredMixin


from .forms import RegisterForm,UserLoginForm,OrderDetailsForm

from .models import Profile, Category, Product, Cart , CartItem, Order, OrderItem,OrderDetails

#main site section
class HomePage(View):
    def get(self,request):
        category = Category.objects.get(name='Phone')
        category1 = Category.objects.get(name='Computer')
        category2 = Category.objects.get(name='Mouse')
        category3 = Category.objects.get(name='Keyboard')
        category4 = Category.objects.get(name='Monitor')
        category5 = Category.objects.get(name='Laptop')
        phones = Product.objects.filter(category=category)
        computer = Product.objects.filter(category=category1)
        mouse = Product.objects.filter(category=category2)
        keyboard = Product.objects.filter(category=category3)
        monitor = Product.objects.filter(category=category4)
        laptop = Product.objects.filter(category=category5)
        categories = Category.objects.all()
        context = {'categories':categories,
                   'phones':phones,
                   'computers':computer,
                   'mouses':mouse,
                   'keyboards':keyboard,
                   'monitors':monitor,
                   'laptops':laptop,
                   }
        return render(request,'main/home_page.html',context)

class ItemPage(View):
    def get(self,request,item_id):
        item = Product.objects.get(id=item_id)
        items = Product.objects.filter(category=item.category)
        context = {'item':item,'items':items}
        return render(request,'main/item_page.html',context)
    
    def post(self,request,item_id):
        cart = self.get_cart()
        product = Product.objects.get(id=item_id)
        item, created = CartItem.objects.get_or_create(product=product, cart=cart)
        if not created:
            item.quantity += 1
            item.save()

        return redirect('cart_page')

    def get_cart(self):
        if self.request.user.is_authenticated:
            profile = Profile.objects.get(user=self.request.user)
            cart, created = Cart.objects.get_or_create(owner=profile)
        else:
            session_key = self.get_session()
            cart, created = Cart.objects.get_or_create(owner=None, session_key=session_key)
        return cart

    
    def get_session(self):
        session_key = self.request.session.session_key
        if not session_key:
            self.request.session.save()
            session_key = self.request.session.session_key
        return session_key
    
    def total_price(self,cart_items):
        t_price = 0
        for item in cart_items:
            if item.quantity > 1:
                t_price += item.product.price*item.quantity
            else:
                t_price += item.product.price
        return t_price
    
class CartPage(ItemPage,View):
    def get(self,request):
        cart = self.get_cart()
        cart_items = CartItem.objects.filter(cart=cart)
        total_price = self.total_price(cart_items)
        context = {'cart_items':cart_items,'total_price':total_price}
        return render(request,'main/cart.html',context)
    
    def post(self, request):
        if 'order' in request.POST:
            cart = self.get_cart()
            cart_items = CartItem.objects.filter(cart=cart)
            return self.create_order(cart, cart_items)
        elif 'item_id' in request.POST:
            item_id = request.POST.get('item_id')
            self.check_quantity(item_id)
        return redirect('cart_page')

    def check_quantity(self, item_id):
        try:
            item = CartItem.objects.get(id=item_id)
            if item.quantity > 1:
                item.quantity -= 1
                item.save()
            else:
                item.delete()
        except CartItem.DoesNotExist:
            return HttpResponse('Item already does not exist')
        
    def create_order(self,cart,cart_items):
        if len(cart_items) != 0:
            if cart.owner:
                order = Order.objects.create(owner=cart.owner)
                self.create_order_items(cart_items,order)   
            else:
                order = Order.objects.create(session_key=cart.session_key)
                self.create_order_items(cart_items,order)
            cart.delete()
            return redirect('order_details_page')
        else:
            return HttpResponse('Your cart is empty')

    def create_order_items(self,cart_items,order):
        for item in cart_items:
            OrderItem.objects.create(product=item.product,order=order,quantity=item.quantity)
            item.delete()
    
class OrderDetailPage(ItemPage,View):
    def get(self,request):
        form = OrderDetailsForm()
        context = {'order_form':form}
        return render(request,'main/order_details.html',context)
    
    def post(self,request):
        form = OrderDetailsForm(request.POST)
        return self.form_validation(form)

    def form_validation(self,form):
        if form.is_valid():
            order_details = form.save(commit=False)
            order = self.get_order()
            order_details.order = order
            order_details.total_price = self.total_price(OrderItem.objects.filter(order=order))
            order_details.save()
            order.status = True
            order.save()
            self.updating_quantity(order)
            return redirect('home_page')
        
    def updating_quantity(self,order):
        for item in OrderItem.objects.filter(order=order):
            quantity = item.quantity
            product = Product.objects.get(id=item.product.id)
            product.quantity -= quantity
            product.save()

    def get_order(self):
        if self.request.user.is_authenticated:
            try:
                order = Order.objects.get(owner=Profile.objects.get(user=self.request.user),status=False)
            except Order.MultipleObjectsReturned:
                order = Order.objects.filter(owner=Profile.objects.get(user=self.request.user),status=False).order_by('created_at').first()
        else:
            try:
                order = Order.objects.get(session_key = self.get_session(),status=False)
            except Order.MultipleObjectsReturned:
                order = Order.objects.filter(session_key = self.get_session(),status=False).order_by('created_at').first()
        return order

class CategoryPage(ItemPage,View):
    def get(self,request,category_id):
        category = Category.objects.get(id=category_id)
        products = Product.objects.filter(
            category=category)
        context = {'products':products,'category':category}
        return render(request,'main/category.html',context)
    
    def post(self,request,category_id):
        if request.method == 'POST':
            item_id = request.POST.get('item_id')
            product = Product.objects.get(id=item_id)
            cart = self.get_cart()
            item, created = CartItem.objects.get_or_create(product=product, cart=cart)
            if not created:
                item.quantity += 1
                item.save()
            return redirect('cart_page')

class ProfilePage(LoginRequiredMixin,View):
    def get(self,request):
        profile = Profile.objects.get(user=request.user)
        orders_list = []
        for order in self.get_orders():
            orders_list.append(OrderDetails.objects.get(order=order))
        context = {'profile':profile,'orders':orders_list}
        return render(request,'main/profile_page.html',context)
    
    def get_orders(self):
        orders = Order.objects.filter(owner=Profile.objects.get(user=self.request.user),status=True)
        return orders
    
#authentication views section

class RegisterPage(View):
    def get(self,request):
        form = RegisterForm()
        context = {'register_form':form}
        return render(request,'main/register_page.html',context)

    def post(self,request):
        form = RegisterForm(request.POST)
        return self.form_validation(form,'login_page')
    
    def form_validation(self,form,succes_url):
        if form.is_valid():
            user = form.save()
            Profile.objects.create(
                user = user,
                firstname = user.first_name,
                lastname = user.last_name,
                email = user.email,
            )
            return redirect(succes_url)
        else:
            return HttpResponse('Invalid data try again later')

class LoginPage(View):
    def get(self,request):
        form = UserLoginForm()
        context = {'login_form':form}
        return render(request,'main/login_page.html',context)
    
    def post(self,request):
        form = UserLoginForm(request,data=request.POST)
        return  self.form_validation(form,'home_page')
    
    def form_validation(self,form,succes_url):
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:
                login(self.request,user)
                return redirect(succes_url)
            else:
                return HttpResponse('Invalid data try again later')
        else:
            return HttpResponse('Invalid data try again later')
        

class LogoutRequest(LoginRequiredMixin,View):
    def get(self,request):
        logout(request)
        return redirect('home_page')
    

#REST API
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ProductSerializer, CategorySerializer,OrderSerializer,ProfileSerializer,UserSerializer
from django.contrib.auth.models import User

@api_view(['GET'])
def getProducts(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getProduct(request,category_id):
    category = Category.objects.get(id=category_id)
    products = Product.objects.filter(category=category)
    serializer = ProductSerializer(products,many=True)
    return Response(serializer.data)

@api_view(['POST'])
def addProduct(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['GET'])
def getCategory(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getOrders(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getProfiles(request):
    profiles = Profile.objects.all()
    serializer = ProfileSerializer(profiles,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users,many=True)
    return Response(serializer.data)