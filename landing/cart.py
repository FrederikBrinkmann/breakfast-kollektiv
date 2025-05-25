from decimal import Decimal
from django.conf import settings
from .models import Product


class Cart:
    def __init__(self, request):
        """
        Initialize the cart with the current session.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, size='M', override_quantity=False):
        """
        Add a product to the cart or update its quantity.
        """
        product_id = str(product.id)
        # Create a unique key for product + size combination
        cart_key = f"{product_id}_{size}"
        
        if cart_key not in self.cart:
            self.cart[cart_key] = {
                'product_id': product_id,
                'quantity': 0,
                'price': str(product.price),
                'size': size,
                'name': product.name,
                'image_front': product.image_front.url if product.image_front else None
            }
        
        if override_quantity:
            self.cart[cart_key]['quantity'] = quantity
        else:
            self.cart[cart_key]['quantity'] += quantity
        
        self.save()

    def save(self):
        """
        Mark the session as modified to ensure it's saved.
        """
        self.session.modified = True

    def remove(self, product, size='M'):
        """
        Remove a product from the cart.
        """
        product_id = str(product.id)
        cart_key = f"{product_id}_{size}"
        
        if cart_key in self.cart:
            del self.cart[cart_key]
            self.save()

    def __iter__(self):
        """
        Iterate over cart items and get products from the database.
        """
        product_ids = [item['product_id'] for item in self.cart.values()]
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        
        for product in products:
            for key, item in cart.items():
                if item['product_id'] == str(product.id):
                    item['product'] = product
                    item['total_price'] = Decimal(item['price']) * item['quantity']
                    yield item

    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Calculate the total price of all items in the cart.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """
        Remove cart from session.
        """
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def get_item_count(self):
        """
        Get the total number of different items (not quantity) in cart.
        """
        return len(self.cart)
