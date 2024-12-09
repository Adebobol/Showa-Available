from rest_framework import serializers
from .models import Cart
from Restaurants.serializers import DishSerializer
from Users.serializers import UserSerializer


class CartSerializer(serializers.ModelSerializer):
    dishes = DishSerializer(many=True)
    user = UserSerializer()

    class Meta:
        model = Cart
        fields = ['dishes', 'user', 'subtotal', 'total']
