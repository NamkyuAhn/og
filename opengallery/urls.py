from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include

urlpatterns = [
    path('main', include('og.urls')),
    path('accounts', include('accounts.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
