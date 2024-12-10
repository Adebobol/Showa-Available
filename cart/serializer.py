from rest_framework import serializers
from .models import Cart, Order
from Restaurants.serializers import DishSerializer
from Users.serializers import UserSerializer


class CartSerializer(serializers.ModelSerializer):
    dishes = DishSerializer(many=True)
    user = UserSerializer()

    class Meta:
        model = Cart
        fields = ['dishes', 'user', 'subtotal',
                  'total', "timestamp", "updated"]


class OrderSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    cart = CartSerializer()

    class Meta:
        model = Order
        fields = ['owner', 'cart', 'delivery_address',
                  'status', "active", "delivery_fee", "total_amount", "updated_time", "created_time"]
