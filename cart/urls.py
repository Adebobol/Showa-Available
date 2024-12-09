from django.urls import path
from .import views


urlpatterns = [
    path('cart/', views.cart_detail_get),
    path('cart/checkout/', views.cart_checkout)
]
