from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from core.views import index, contact

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('contact', contact, name='contact'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
