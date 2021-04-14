from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

# App name route
app_name = "backend"

# Project URL paths
urlpatterns = [
    path('', views.index, name="index"),
    
    path('results', views.results, name="results"),
    path('search', views.search, name="search"),
    path('store-data', views.store_data, name="store_data"),
    path('store-counts', views.load_lang_counts, name="load_lang_counts"),
    path('test_maps/regions', views.test_maps_regions, name='test_maps_regions'),
    path("tsne", views.tsne_search, name="tsne")

]