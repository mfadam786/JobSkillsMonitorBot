from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

# App name route
app_name = "backend"

# Project URL paths
urlpatterns = [
    path('', views.index, name="index"),
    path('store-data', views.store_data, name="store_data"),
    path('test_maps', views.test_maps, name='test_maps')
]