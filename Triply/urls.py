"""
URL configuration for Triply project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({"status": "Triply Backend is running!"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', health_check),
    
    # API v1 endpoints
    path('api/v1/auth/', include('accounts.api.urls')),
    path('api/v1/trips/', include('trips.api.urls')),
    path('api/v1/itineraries/', include('itineraries.api.urls')),
    path('api/v1/budgets/', include('budgets.api.urls')),
    path('api/v1/documents/', include('documents.api.urls')),        # Add this
    path('api/v1/collaboration/', include('collaboration.api.urls')), # Add this
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)