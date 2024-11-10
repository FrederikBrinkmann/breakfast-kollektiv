
# mywebsite/urls.py

from django.contrib import admin
from django.urls import path
from landing import views  # Importiere die Views aus der landing-App
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.landing_page, name='landing'),  # Leere URL für die Landing Page
    path('musik-events/', views.musik_events, name='musik_events'),
    path('shop/', views.shop, name='shop'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),  # Product detail page
    path('impressum/', views.impressum, name='impressum'),
    path('galerie/', views.galerie, name='galerie'),
    path('checkout/', views.checkout, name='checkout'),
    path('process-checkout/', views.process_checkout, name='process_checkout'),
    path('uberuns/', views.uberuns, name='uberuns'),  # Füge diese Zeile hinzu
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)