from django.shortcuts import render
from landing import views

# landing/views.py
def landing_page(request):
    return render(request, 'landing/landing.html')

def musik_events(request):
    return render(request, 'landing/musik_events.html')

def shop(request):
    return render(request, 'landing/shop.html')