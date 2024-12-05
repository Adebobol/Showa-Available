from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('api/restaurants/', views.RestaurantList.as_view(), name='restaurant-list')
]
