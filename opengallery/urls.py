from django.urls import path, include

urlpatterns = [
    path('', include('og.urls')),
    path('accounts', include('accounts.urls')),
]
