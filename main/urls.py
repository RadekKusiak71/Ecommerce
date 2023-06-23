from django.urls import path
from . import views

urlpatterns = [
    path('',views.HomePage.as_view(),name='home_page'),

    # Authentication urls
    path('register/',views.RegisterPage.as_view(),name='register_page'),
    path('login/',views.LoginPage.as_view(),name='login_page'),
    path('logout/',views.LogoutRequest.as_view(),name='logout_request'),
]