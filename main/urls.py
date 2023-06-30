from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.HomePage.as_view(),name='home_page'),
    path('profile',views.ProfilePage.as_view(),name='profile_page'),
    path('category/<int:category_id>',views.CategoryPage.as_view(),name='category_page'),
    path('item/<int:item_id>/',views.ItemPage.as_view(),name='item_page'),
    path('cart',views.CartPage.as_view(),name='cart_page'),
    path('order/',views.OrderDetailPage.as_view(),name='order_details_page'),
    # Authentication urls
    path('register/',views.RegisterPage.as_view(),name='register_page'),
    path('login/',views.LoginPage.as_view(),name='login_page'),
    path('logout/',views.LogoutRequest.as_view(),name='logout_request'),

    # REST API

    #GET APIS
    path('api/products',views.getProducts),
    path('api/products/<int:category_id>',views.getProduct),
    path('api/category',views.getCategory),
    path('api/profiles',views.getProfiles),
    path('api/users',views.getUsers),
    path('api/order',views.getOrders),
    path('api/order/<int:order_id>',views.getOrderItems),

    #POST APIS
    path('api/productadd',views.addProduct),
    

    #

    ]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)