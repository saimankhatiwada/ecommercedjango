from django.urls import path

from . import views

app_name = "meropasal"
urlpatterns = [
    path('', views.home, name='home'),
    path('products', views.product, name='product'),
]
