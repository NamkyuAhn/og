from django.urls import path, include

urlpatterns = [
    path('main', include('og.urls')),
    path('accounts', include('accounts.urls')),
]
