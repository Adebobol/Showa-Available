from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('restaurant/', views.RestaurantList.as_view()),
    path('restaurant/<int:pk>/', views.RestaurantDetail.as_view()),
    path('restaurant/<int:pk>/dishes/', views.DishList.as_view()),
    path('restaurant/<int:pk>/dishes/<str:name>/', views.DishDetail.as_view()),
    # path('restaurant/<int:pk>/dishes/<str:name>/', views.DishDetail.as_view()),
]
