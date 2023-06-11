from django.shortcuts import render
from django.views import generic

from .models import Product

def home(request):
    return render(request, "Main/home.html")


class IndexProductView(generic.ListView):
    template_name = "Product/products.html"
    context_object_name = "product_list"
    
    def get_queryset(self):
        return Product.objects.all()

class DetailProductView(generic.DetailView):
    model = Product
    template_name = "Product/productsdetail.html"

