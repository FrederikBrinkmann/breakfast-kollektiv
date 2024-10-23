from django.shortcuts import render
from landing import views
from .models import Event
from.models import Product

# landing/views.py
def landing_page(request):
    return render(request, 'landing/landing.html')

def musik_events(request):
    events = Event.objects.all().order_by('-date')  # Most recent events first
    return render(request, 'landing/musik_events.html', {'events': events})

def shop(request):
    return render(request, 'landing/shop.html') 

def galerie(request):
    return render(request, 'landing/galerie.html')

def impressum(request):
    return render(request, 'landing/impressum.html')

def shop(request):
    products = Product.objects.all()
    return render(request, 'landing/shop.html', {'products': products})
