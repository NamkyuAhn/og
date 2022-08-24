from django.urls import path, include
from . import views

app_name = 'og'

urlpatterns = [
	path('', views.main, name = 'main'),
	path('/artist_entry', views.artist_entry, name = 'artist_entry'),
	path('/artist_menu', views.artist_menu, name = 'artist_menu'),
]