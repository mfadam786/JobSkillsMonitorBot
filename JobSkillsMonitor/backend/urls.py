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
    path('test_maps/regions', views.test_maps_regions, name='test_maps_regions'),
    path("tsne", views.tsne_search, name="tsne")

]