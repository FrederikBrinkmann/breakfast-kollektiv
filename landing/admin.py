from django.contrib import admin

# Register your models here.

from .models import Event, Product

admin.site.register(Event)

admin.site.register(Product) 