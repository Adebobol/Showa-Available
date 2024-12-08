from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.register, name="register-user"),
    path('api/users/', views.UserListView.as_view(), name='user-get')
]
