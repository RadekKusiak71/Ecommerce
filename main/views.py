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
        categories = Category.objects.all()
        context = {'categories':categories}
        return render(request,'main/home_page.html',context)

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