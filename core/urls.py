"""
Family Expenditure Management System - Main URL Configuration
Root URL patterns for the entire project
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    
    # Expenses App URLs (includes both API and template views)
    path("expenses/", include("expenses.urls")),
    
    # Redirect root to login
    path("", RedirectView.as_view(url="/expenses/login/", permanent=False)),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
