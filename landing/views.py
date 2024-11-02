from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Product, Order, Event
from .forms import CheckoutForm
from django.core.mail import send_mail
from django.conf import settings

# Views for your landing page and event handling
def landing_page(request):
    return render(request, 'landing/landing.html')

def musik_events(request):
    events = Event.objects.all().order_by('-date')  # Most recent events first
    return render(request, 'landing/musik_events.html', {'events': events})

def shop(request):
    products = Product.objects.all()
    return render(request, 'landing/shop.html', {'products': products})

def galerie(request):
    return render(request, 'landing/galerie.html')

def impressum(request):
    return render(request, 'landing/impressum.html')

# Product detail view
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'landing/product_detail.html', {'product': product})

# Checkout view
def checkout(request):
    product_id = request.GET.get('product_id')
    size = request.GET.get('size')

    if not product_id or not size:
        messages.error(request, 'Produkt oder Größe fehlt.')
        return redirect('shop')

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        messages.error(request, 'Produkt nicht gefunden.')
        return redirect('shop')

    # Initialize the form with product_id and size
    form = CheckoutForm(initial={'product_id': product_id, 'size': size})
    return render(request, 'landing/checkout.html', {'form': form, 'product': product, 'size': size})

# Process checkout view
def process_checkout(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST)

        if form.is_valid():
            # Extract cleaned data from the form
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            address = form.cleaned_data['address']
            size = form.cleaned_data['size']
            product_id = form.cleaned_data['product_id']

            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                messages.error(request, 'Produkt nicht gefunden.')
                return redirect('shop')

            # Calculate total price
            total_price = product.price

            # Save the order
            order = Order(
                user=request.user if request.user.is_authenticated else None,
                name=name,
                email=email,
                address=address,
                product=product,
                size=size,
                total_price=total_price
            )
            order.save()

            # Send a confirmation email
            send_mail(
                'Bestellbestätigung',
                f'Hallo {name},\n\nIhre Bestellung für {product.name} (Größe: {size}) wurde erfolgreich abgeschlossen. Vielen Dank für Ihren Einkauf!',
                settings.EMAIL_HOST_USER, 
                [email],
                fail_silently=False,
            )

            # Success message and redirect
            messages.success(request, 'Bestellung erfolgreich abgeschlossen!')
            return redirect('landing_page')
        else:
            # If the form is not valid, show errors
            messages.error(request, 'Bitte füllen Sie alle Felder korrekt aus.')
            return render(request, 'landing/checkout.html', {'form': form})

    return HttpResponse('Ungültige Anfrage', status=400)
