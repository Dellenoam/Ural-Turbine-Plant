from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from access_system import settings

urlpatterns = [
    path('', include('core.urls')),
    path('', include('accounts.urls')),
    path('', include('access_office.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
