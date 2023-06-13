from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic
from django.db import IntegrityError
from django.urls import reverse


from .models import Product, ContactUs, Blogs, KeyFeatures

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
    
    def get_context_data(self, **kwargs) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context['product'] = self.get_object()
        return context
    
class IndexBlogView(generic.ListView):
    template_name = "Blog/blogs.html"
    context_object_name = "blog_list"
    
    def get_queryset(self):
        return Blogs.objects.all()
    
class DetailBlogView(generic.DetailView):
    model = Blogs
    template_name = "Blog/blogsdetail.html"
    
    def get_context_data(self, **kwargs) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        blog = self.get_object()
        key_features = KeyFeatures.objects.filter(blog=blog)
        context['blog'] = blog
        context['key_feature_list'] = key_features
        return context



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
