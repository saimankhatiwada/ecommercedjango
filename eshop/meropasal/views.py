import json
from django.http import HttpRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.db import IntegrityError
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


from .models import Product, ContactUs, Blogs, KeyFeatures, Cart, CartItems, KhaltiPaymentStatus
import requests



def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("meropasal:home"))
            else:
                error_message = 'Invalid username or password.'
                return render(request, 'Login/login.html', {'error_message': error_message, 'username': username})
            
        except Exception as e:
            error_message = e
            return render(request, 'Login/login.html', {'error_message': error_message, 'username': username})
    
    else:
        return render(request, "Login/login.html")





def register_user(request):
    if request.method == "POST":
        
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password != confirm_password:
            error_message = 'Passwords do not match.'
            return render(request, 'Registration/registration.html', {'error_message': error_message, 'username': username,
            'email': email})
        
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            return HttpResponseRedirect(reverse("meropasal:home"))
        
        except IntegrityError:
            error_message = "Username already exists"
            return render(request, 'Registration/registration.html', {'error_message': error_message, 'username': username,
            'email': email})
            
        except Exception as e:
            error_message = e
            return render(request, 'Registration/registration.html', {'error_message': error_message, 'username': username,
            'email': email})
    
    else:
        return render(request, "Registration/registration.html")




def logout_user(request):
    logout(request)
    return render(request, "Main/home.html")




def home(request):
    return render(request, "Main/home.html")




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




@login_required(login_url="http://0.0.0.0:8000/login/")
def add_to_cart(request, id):
    user = request.user
    product = get_object_or_404(Product, id=id)
    cart, _ = Cart.objects.get_or_create(user=user, is_paid=False)
    cart_item, cart_created = CartItems.objects.get_or_create(cart=cart, product=product)
    if not cart_created:
        cart_item.count += 1
        cart_item.save()
    return HttpResponseRedirect(reverse("meropasal:product"))




@login_required(login_url="http://0.0.0.0:8000/login/")
def shopping_cart(request):
    try:
        user = request.user
        cart = Cart.objects.get(user=user)
        cart_items = CartItems.objects.filter(cart=cart)
        grand_total = 0
        
        for item in cart_items:
            grand_total += item.get_product_total_price()
            
        context = {
            'cart': cart,
            'cart_items': cart_items,
            'cart_grand_total': grand_total
        }
        
        return render(request, "Carts/cart.html", context)
    except Exception:
        pass
    
    return render(request, "Carts/cart.html")
    

def increase_cart_item_count(request, item_id):
    try:
        item = CartItems.objects.get(id=item_id)
        item.count += 1
        item.save()
        return HttpResponseRedirect(reverse("meropasal:cart"))
    except CartItems.DoesNotExist:
        return HttpResponseRedirect(reverse("meropasal:cart"))
    
    
def deacrease_cart_item_count(request, item_id):
    try:
        item = get_object_or_404(CartItems, id=item_id)
        if item.count <= 1:
            item.delete()
        else:
            item.count -= 1
            item.save()
        return HttpResponseRedirect(reverse("meropasal:cart"))
    
    except CartItems.DoesNotExist:
        return HttpResponseRedirect(reverse("meropasal:cart"))


def khalti_checkout(request):
    
    user = request.user
    cart_shopping = Cart.objects.get(user=user)
    cart_items = CartItems.objects.filter(cart=cart_shopping)
    grand_total = 0
    
    for item in cart_items:
        grand_total += item.get_product_total_price()
        
    amount = grand_total
    
    headers = {
        'Authorization': "Key 6531a9fd7d54409c9ae878687dd27dae",
        'Content-Type': 'application/json'
    }
    
    url = "https://a.khalti.com/api/v2/epayment/initiate/"
    
    data = {
        "return_url": "http://0.0.0.0:8000/khalticheckout/verify",
        "website_url": "http://0.0.0.0:8000",
        "amount": amount * 100,
        "purchase_order_id": f"{cart_shopping.id}",
        "purchase_order_name": f"{cart_shopping.user.username}",
        "customer_info": {
            "name": cart_shopping.user.username,
            "email": cart_shopping.user.email,
            "phone": "9811496763"
        }
    }
    json_data = json.dumps(data, default=str)
    response = requests.post(url,headers=headers,data=json_data)
    response_data = response.json()
    khalti_payment_status = KhaltiPaymentStatus(
        pidx = response_data['pidx'],
        user = cart_shopping.user,
        cart = cart_shopping 
    )
    khalti_payment_status.save()
    return HttpResponseRedirect(response_data['payment_url'])
    
    
def khalti_checkout_verify(request):
    user = request.user
    cart_shopping = Cart.objects.get(user=user)
    payment_status = get_object_or_404(KhaltiPaymentStatus, user=user)
    headers = {
        'Authorization': "Key 6531a9fd7d54409c9ae878687dd27dae",
        'Content-Type': 'application/json'
    }
    url = "https://a.khalti.com/api/v2/epayment/lookup/"
    
    data = {
        "pidx": f"{payment_status.pidx}",
    }
    
    json_data = json.dumps(data, default=str)
    response = requests.post(url,headers=headers,data=json_data)
    response_data = response.json()
    
    if response_data['status'] == "Completed":
        payment_status.delete()
        cart_shopping.delete()
        return HttpResponseRedirect(reverse("meropasal:product"))
    
    else:
        payment_status.delete()
        return HttpResponseRedirect(reverse("meropasal:cart"))
        
        

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



