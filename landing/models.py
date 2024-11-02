from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField()
    location = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(blank=True, upload_to='events/')
    youtube_url = models.URLField(blank=True, null=True)
    soundcloud_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_front = models.ImageField(upload_to='products/')  # Front image
    image_back = models.ImageField(upload_to='products/', blank=True, null=True)  # Back image (optional)

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.TextField()
    size = models.CharField(max_length=10)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Add this line
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order by {self.name} for {self.product.name}"
