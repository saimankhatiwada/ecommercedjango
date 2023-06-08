from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return render(request, "Main/home.html")


def product(request):
    return render(request, "Product/products.html")
