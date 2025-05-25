# landing/forms.py

from django import forms

class CheckoutForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, label='Name')
    email = forms.EmailField(required=True, label='E-Mail')
    address = forms.CharField(max_length=255, required=True, label='Adresse')
    size = forms.CharField(widget=forms.HiddenInput())  # Hidden input for size
    product_id = forms.CharField(widget=forms.HiddenInput())  # Hidden input for product ID

class CartCheckoutForm(forms.Form):
    """Form for checkout with multiple items from cart"""
    name = forms.CharField(
        max_length=100, 
        required=True, 
        label='Vollständiger Name',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Max Mustermann'
        })
    )
    email = forms.EmailField(
        required=True, 
        label='E-Mail-Adresse',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'max@beispiel.de'
        })
    )
    phone = forms.CharField(
        max_length=20,
        required=False,
        label='Telefonnummer (optional)',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+49 123 456789'
        })
    )
    street_address = forms.CharField(
        max_length=255, 
        required=True, 
        label='Straße und Hausnummer',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Musterstraße 123'
        })
    )
    postal_code = forms.CharField(
        max_length=10, 
        required=True, 
        label='Postleitzahl',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '12345'
        })
    )
    city = forms.CharField(
        max_length=100, 
        required=True, 
        label='Stadt',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Berlin'
        })
    )
    country = forms.CharField(
        max_length=100, 
        required=True, 
        label='Land',
        initial='Deutschland',
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )
    notes = forms.CharField(
        required=False,
        label='Anmerkungen (optional)',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Besondere Wünsche oder Anmerkungen...'
        })
    )
