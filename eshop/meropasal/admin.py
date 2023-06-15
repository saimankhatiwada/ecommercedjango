from django.contrib import admin

from .models import Category, Product, Blogs, KeyFeatures, Cart, CartItems, KhaltiPaymentStatus

class FeatureInline(admin.TabularInline):
    model = KeyFeatures
    extra = 1
    
class BlogAdmin(admin.ModelAdmin):
    inlines = [FeatureInline]

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Blogs, BlogAdmin)
admin.site.register(Cart)
admin.site.register(CartItems)
admin.site.register(KhaltiPaymentStatus)
