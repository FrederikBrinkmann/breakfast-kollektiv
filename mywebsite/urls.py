
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
    path('impressum/', views.impressum, name='impressum'),
    path('galerie/', views.galerie, name='galerie'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)