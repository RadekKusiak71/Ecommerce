from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views import View
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin


from .forms import RegisterForm,UserLoginForm

from .models import Profile, Category, Product, Cart , CartItem, Order, OrderItem, Order_details

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