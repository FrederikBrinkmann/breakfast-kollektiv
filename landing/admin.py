from django.contrib import admin
from .models import Event, Product, Order

# Customize the Event admin interface
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'location')  # Display these fields in the list view
    search_fields = ('name', 'location')  # Add a search bar for easier navigation
    list_filter = ('date', 'location')  # Add filters for the date and location fields

# Customize the Product admin interface
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'image_front', 'image_back')  # Display these fields in the list view
    search_fields = ('name', 'description')  # Add a search bar for the name and description
    list_filter = ('price',)  # Add a filter for the price field

# Add Order admin interface
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'email', 'address', 'get_sizes', 'total_price', 'created_at')
    search_fields = ('name', 'email')
    list_filter = ('created_at', 'user')

    def get_sizes(self, obj):
        # Alle Größen der OrderItems für diese Order als Komma-Liste ausgeben
        return ", ".join([item.size for item in obj.items.all() if item.size])
    get_sizes.short_description = 'Größen'
