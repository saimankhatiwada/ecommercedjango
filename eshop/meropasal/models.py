import os
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.postgres.fields import ArrayField
from uuid import uuid4

def get_product_image_path(instance, filename) -> str:
    file_extension = os.path.splitext(filename)[1]
    unique_filename = f'{instance.id}{file_extension}'
    return os.path.join('eshop', 'meropasal', 'static', 'products', unique_filename)

def get_blog_image_path(instance, filename) -> str:
    file_extension = os.path.splitext(filename)[1]
    unique_filename = f'{instance.id}{file_extension}'
    return os.path.join('eshop', 'meropasal', 'static', 'blogs', unique_filename)

def validate_image_file_extension(value) -> Exception | None:
    if not value.name.endswith('.jpg'):
        raise ValidationError("Only JPEG files are allowed.")


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=100)
    created_date = models.DateTimeField("Created date",auto_now_add=True)
    updated_date = models.DateTimeField("Updated date", auto_now=True)
    
    def __str__(self) -> str:
        return self.name

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField("Name", max_length=100)
    description = models.TextField("Description", max_length=1000)
    product_img_url = models.ImageField("Product image",upload_to=get_product_image_path, validators=[validate_image_file_extension])
    product_img_name = models.CharField(max_length=100, unique=True, blank= True, null=True, editable=False)
    price = models.DecimalField("Price", max_digits=10, decimal_places=2)
    stock = models.IntegerField("Stock", null=True)
    created_date = models.DateTimeField("Created date",auto_now_add=True)
    updated_date = models.DateTimeField("Updated date", auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        self.product_img_name = f"{self.id}.jpg"
        super().save(*args, **kwargs)
        
    def delete(self, *args, **kwargs):
        if self.product_img_url:
            if os.path.exists(self.product_img_url.path):
                os.remove(self.product_img_url.path)
        super().delete(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.name
    

class ContactUs(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    contact_name = models.CharField("Name", max_length=100)
    contatc_email = models.EmailField("Email", unique=True, max_length=200)
    contact_message = models.TextField("Message", max_length=1000)
    created_date = models.DateTimeField("Created date",auto_now_add=True)
    
    def __str__(self) -> str:
        return self.contact_name
    
    

    
class Blogs(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    blog_name = models.CharField("Name", max_length=300)
    blog_description = models.TextField("Description", max_length=2000)
    blog_img_url = models.ImageField("Blog image", upload_to=get_blog_image_path, validators=[validate_image_file_extension])
    blog_img_name = models.CharField(max_length=200, unique=True, blank= True, null=True, editable=False)
    created_date = models.DateTimeField("Created date",auto_now_add=True)
    updated_date = models.DateTimeField("Updated date", auto_now=True)
    
    def save(self, *args, **kwargs):
        self.blog_img_name = f"{self.id}.jpg"
        super().save(*args, **kwargs)
        
    def delete(self, *args, **kwargs):
        if self.blog_img_url:
            if os.path.exists(self.blog_img_url.path):
                os.remove(self.blog_img_url.path)
        super().delete(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.blog_name
    

class KeyFeatures(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid4,editable=False)
    blog = models.ForeignKey(Blogs, on_delete=models.CASCADE)
    features = models.TextField(max_length=1000)
    
    def __str__(self) -> str:
        return self.features
    