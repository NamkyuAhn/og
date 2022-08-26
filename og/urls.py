from django.urls import path
from . import views

app_name = 'og'

urlpatterns = [
	path('', views.main, name = 'main'),
	path('/artist_list', views.artist_list, name = 'artist_list'),
	path('/item_list', views.item_list, name = 'item_list'),

	path('/artist_entry', views.artist_entry, name = 'artist_entry'),
	path('/artist_menu', views.artist_menu, name = 'artist_menu'),
	path('/item_entry', views.item_entry, name = 'item_entry'),
	path('/exhibition_entry', views.exhibition_entry, name = 'exhibition_entry'),

	path('/admin', views.admin_menu, name = 'admin_menu'),
	path('/admin/artist_stat', views.artist_stat, name = 'artist_stat'),
]