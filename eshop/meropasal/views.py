from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic
from django.db import IntegrityError
from django.urls import reverse

from .models import Product, ContactUs

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


def contactus(request):
    if request.method == "POST":
        try:
            contact_us = ContactUs(
                contact_name=request.POST["contact_name"],
                contatc_email=request.POST["contatc_email"],
                contact_message=request.POST["contact_message"]
            )
            contact_us.save()
        
        except IntegrityError:
            pass
        
        return HttpResponseRedirect(reverse("meropasal:product"))
    
    else:
        return render(request, "ContactUs/contact.html")
