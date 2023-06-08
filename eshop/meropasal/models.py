from django.db import models
from uuid import uuid4


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return self.name

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField("Name", max_length=100)
    description = models.TextField("Description", max_length=1000)
    product_img = models.ImageField("Product image", upload_to='products/')
    price = models.DecimalField("Price", max_digits=10, decimal_places=2)
    created_date = models.DateTimeField("Created date",auto_now_add=True)
    updated_date = models.DateTimeField("Updated date", auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    
    def __str__(self) -> str:
        return self.name
