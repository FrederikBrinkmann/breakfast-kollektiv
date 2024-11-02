# landing/forms.py

from django import forms

class CheckoutForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, label='Name')
    email = forms.EmailField(required=True, label='E-Mail')
    address = forms.CharField(max_length=255, required=True, label='Adresse')
    size = forms.CharField(widget=forms.HiddenInput())  # Hidden input for size
    product_id = forms.CharField(widget=forms.HiddenInput())  # Hidden input for product ID
