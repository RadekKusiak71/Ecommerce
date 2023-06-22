from django.shortcuts import render
from django.views import View

class HomePage(View):
    def get(self,request):
        context = {}
        return render(request,'main/home_page.html',context)