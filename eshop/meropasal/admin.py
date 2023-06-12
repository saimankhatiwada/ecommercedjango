from django.contrib import admin

from .models import Category, Product, Blogs

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Blogs)