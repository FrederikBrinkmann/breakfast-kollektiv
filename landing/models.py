from django.db import models

# Create your models here.
from django.db import models

class Event(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField()
    location = models.CharField(max_length=200)
    description = models.TextField(blank= True)
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
