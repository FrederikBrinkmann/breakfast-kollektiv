from django.db import models
from django.contrib.auth.models import User
from datetime import date 

class Event(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField()
    location = models.CharField(max_length=200)
    start_time = models.TimeField(null=True, blank=True)  # Startzeit für das Event
    end_time = models.TimeField(null=True, blank=True) 
    description = models.TextField(blank=True)
    image = models.ImageField(blank=True, upload_to='events/')
    youtube_url = models.URLField(blank=True, null=True)
    soundcloud_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name
    
    @classmethod
    def upcoming_events(cls):
        """Returns upcoming events sorted by date."""
        return cls.objects.filter(date__gte=date.today()).order_by('date')

    @classmethod
    def past_events(cls):
        """Returns past events sorted by date descending."""
        return cls.objects.filter(date__lt=date.today()).order_by('-date')
    
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
    phone = models.CharField(max_length=20, blank=True, null=True)
    street_address = models.CharField(max_length=255, default='')
    postal_code = models.CharField(max_length=10, default='')
    city = models.CharField(max_length=100, default='')
    country = models.CharField(max_length=100, default='Deutschland')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    order_number = models.CharField(max_length=20, unique=True, blank=True)
    
    # Legacy field for backwards compatibility
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Order #{self.order_number} by {self.name} ({self.created_at.date()})"
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            # Generate order number like BK-2024-001
            from datetime import datetime
            year = datetime.now().year
            last_order = Order.objects.filter(
                order_number__startswith=f'BK-{year}-'
            ).order_by('-id').first()
            
            if last_order:
                last_num = int(last_order.order_number.split('-')[-1])
                new_num = last_num + 1
            else:
                new_num = 1
            
            self.order_number = f'BK-{year}-{new_num:03d}'
        
        super().save(*args, **kwargs)
    
    def get_full_address(self):
        """Return formatted full address"""
        return f"{self.street_address}\n{self.postal_code} {self.city}\n{self.country}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=10, blank=True, null=True)

    def get_total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
