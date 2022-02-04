from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from cheque_service import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('chequeapp.urls')),
    path('silk/', include('silk.urls', namespace='silk')),
    path('django-rq/', include('django_rq.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
