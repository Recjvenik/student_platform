"""
URL configuration for Student Training & Job Platform
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import HomeView

# Dashboard URL at root level
from django.urls import path
from students.views import dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('accounts/', include('allauth.urls')),
    path('', include('accounts.urls')),
    path('profile/', include('students.urls')),
    path('dashboard/', dashboard, name='dashboard'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)