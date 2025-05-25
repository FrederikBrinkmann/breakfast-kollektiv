from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Product, Order, Event, OrderItem
from .forms import CheckoutForm, CartCheckoutForm
from django.core.mail import send_mail
from django.conf import settings
from datetime import date
from .cart import Cart
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from ics import Calendar, Event as ICSEvent
from datetime import datetime

# Views for your landing page and event handling
def landing_page(request):
    return render(request, 'landing/landing.html')


def musik_events(request):
    upcoming_events = Event.upcoming_events()  # Fetch upcoming events
    past_events = Event.past_events()  # Fetch past events

    return render(request, 'landing/musik_events.html', {
        'upcoming_events': upcoming_events,
        'past_events': past_events
    })

def download_ics(request, event_id):
    # Hole das Event-Objekt
    event = get_object_or_404(Event, id=event_id)

    # Erstelle einen ICS-Kalender
    calendar = Calendar()
    ics_event = ICSEvent()

    # Setze die Event-Daten für das ICS-Event
    ics_event.name = event.name
    ics_event.description = event.description
    ics_event.location = event.location

    # Kombiniere Datum und Uhrzeit für Start und Ende des Events
    start_datetime = datetime.combine(event.date, event.start_time) if event.start_time else event.date
    end_datetime = datetime.combine(event.date, event.end_time) if event.end_time else None

    ics_event.begin = start_datetime.isoformat()
    
    # Falls eine Endzeit definiert ist, füge sie hinzu
    if end_datetime:
        ics_event.end = end_datetime.isoformat()

    # Füge das Event zum Kalender hinzu
    calendar.events.add(ics_event)

    # Konvertiere den Kalender in eine ICS-Datei und bereite den Download vor
    response = HttpResponse(calendar.serialize(), content_type="text/calendar")
    response['Content-Disposition'] = f'attachment; filename="{event.name}.ics"'
    return response


def uberuns(request):
    return render(request, 'landing/uberuns.html')

def shop(request):
    products = Product.objects.all()
    return render(request, 'landing/shop.html', {'products': products})

def galerie(request):
    return render(request, 'landing/galerie.html')

def impressum(request):
    return render(request, 'landing/impressum.html')

# Product detail view with related products
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    # Fetch related products, excluding the current product, and limit to 4
    related_products = Product.objects.exclude(pk=pk)[:4]

    return render(request, 'landing/product_detail.html', {
        'product': product,
        'related_products': related_products
    })

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
            return redirect('landing')
        else:
            # If the form is not valid, show errors
            messages.error(request, 'Bitte füllen Sie alle Felder korrekt aus.')
            return render(request, 'landing/checkout.html', {'form': form})

    return HttpResponse('Ungültige Anfrage', status=400)

# Cart views
def cart_detail(request):
    """Display cart contents"""
    cart = Cart(request)
    return render(request, 'landing/cart.html', {'cart': cart})

@require_POST
def cart_add(request, product_id):
    """Add product to cart"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    size = request.POST.get('size', 'M')
    quantity = int(request.POST.get('quantity', 1))
    
    cart.add(product=product, quantity=quantity, size=size)
    
    # Return JSON response for AJAX requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_count': len(cart),
            'message': f'{product.name} wurde zum Warenkorb hinzugefügt!'
        })
    
    messages.success(request, f'{product.name} wurde zum Warenkorb hinzugefügt!')
    return redirect('product_detail', pk=product_id)

@require_POST
def cart_remove(request, product_id):
    """Remove product from cart"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    size = request.POST.get('size', 'M')
    
    cart.remove(product, size)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_count': len(cart),
            'cart_total': str(cart.get_total_price())
        })
    
    return redirect('cart_detail')

def cart_clear(request):
    """Clear entire cart"""
    cart = Cart(request)
    cart.clear()
    return redirect('cart_detail')

def cart_context_processor(request):
    """Context processor to make cart available in all templates"""
    return {'cart': Cart(request)}

# Cart-based checkout views
def cart_checkout(request):
    """Display checkout form for cart items"""
    cart = Cart(request)
    
    if len(cart) == 0:
        messages.error(request, 'Ihr Warenkorb ist leer.')
        return redirect('cart_detail')
    
    form = CartCheckoutForm()
    
    return render(request, 'landing/cart_checkout.html', {
        'form': form,
        'cart': cart,
        'total': cart.get_total_price()
    })

def process_cart_checkout(request):
    """Process the cart checkout form"""
    if request.method == 'POST':
        form = CartCheckoutForm(request.POST)
        cart = Cart(request)
        
        if len(cart) == 0:
            messages.error(request, 'Ihr Warenkorb ist leer.')
            return redirect('cart_detail')
        
        if form.is_valid():
            # Create order
            order = Order(
                user=request.user if request.user.is_authenticated else None,
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                street_address=form.cleaned_data['street_address'],
                postal_code=form.cleaned_data['postal_code'],
                city=form.cleaned_data['city'],
                country=form.cleaned_data['country'],
                notes=form.cleaned_data['notes'],
                total_price=cart.get_total_price()
            )
            order.save()
            
            # Create order items
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity'],
                    size=item['size']
                )
            
            # Send confirmation email
            send_order_confirmation_email(order)
            
            # Clear cart
            cart.clear()
            
            messages.success(request, f'Bestellung erfolgreich! Bestellnummer: {order.order_number}')
            return render(request, 'landing/order_success.html', {'order': order})
        
        else:
            return render(request, 'landing/cart_checkout.html', {
                'form': form,
                'cart': cart,
                'total': cart.get_total_price()
            })
    
    return redirect('cart_checkout')

def send_order_confirmation_email(order):
    """Send order confirmation email"""
    try:
        # Email to customer
        subject = f'Bestellbestätigung - {order.order_number}'
        
        # Create email content
        email_context = {
            'order': order,
            'order_items': order.items.all()
        }
        
        html_message = render_to_string('landing/emails/order_confirmation.html', email_context)
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[order.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        # Email to shop owner (optional)
        owner_subject = f'Neue Bestellung - {order.order_number}'
        send_mail(
            subject=owner_subject,
            message=f'Neue Bestellung eingegangen:\n\nBestellnummer: {order.order_number}\nKunde: {order.name}\nE-Mail: {order.email}\nGesamtsumme: {order.total_price}€',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.EMAIL_HOST_USER],  # Send to shop email
            fail_silently=True,
        )
        
    except Exception as e:
        print(f"Error sending email: {e}")

def order_success(request):
    """Display order success page"""
    return render(request, 'landing/order_success.html')
