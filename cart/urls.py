from django.urls import path
from .import views


urlpatterns = [
    path('cart/', views.cart_detail_get),
    path('checkout/summary', views.cart_checkout),
    path('checkout/<str:orderId>', views.confirm_order),
    # path('cart/checkout/payment/add', views.confirm_order),
]
