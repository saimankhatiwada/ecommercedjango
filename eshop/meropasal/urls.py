from django.urls import path

from . import views

app_name = "meropasal"
urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('products/', views.IndexProductView.as_view(), name='product'),
    path('products/<uuid:pk>/', views.DetailProductView.as_view(), name='product_detail'),
    path('products/addtocart/<id>/', views.add_to_cart, name='addtocart'),
    path('blogs/', views.IndexBlogView.as_view(), name='blog'),
    path('blogs/<uuid:pk>/', views.DetailBlogView.as_view(), name='blog_detail'),
    path('contactus/', views.contactus, name='contactus'),
    path('cart/', views.shopping_cart, name='cart'),
    path('cart/increase_cart/<item_id>', views.increase_cart_item_count, name='increase_cart'),
    path('cart/decrease_cart/<item_id>', views.deacrease_cart_item_count, name='decrease_cart'),
    path('khalticheckout/', views.khalti_checkout, name='khalti_checkout'),
    path('khalticheckout/verify', views.khalti_checkout_verify, name='khalti_checkout_verify'),
]

