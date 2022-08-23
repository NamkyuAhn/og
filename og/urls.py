from django.urls import path, include
from . import views

app_name = 'og'

urlpatterns = [
	path('', views.main, name='main'),
]