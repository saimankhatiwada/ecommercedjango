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
]

