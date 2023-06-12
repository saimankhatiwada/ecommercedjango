from django.urls import path

from . import views

app_name = "meropasal"
urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.IndexProductView.as_view(), name='product'),
    path('products/<uuid:pk>/', views.DetailProductView.as_view(), name='product_detail'),
    path('contactus/', views.contactus, name='contactus'),
]

