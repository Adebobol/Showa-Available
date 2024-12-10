from rest_framework import serializers
from .models import Cart, Order
from Restaurants.serializers import DishSerializer
from Users.serializers import UserSerializer
from django.contrib.auth.models import User


class CartSerializer(serializers.ModelSerializer):
    dishes = DishSerializer(many=True)
    # user = UserSerializer()
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Cart
        fields = ['dishes', 'user', 'subtotal',
                  'total', "timestamp", "updated"]


class OrderSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    # cart = CartSerializer()
    cart = serializers.PrimaryKeyRelatedField(queryset=Cart.objects.all())

    class Meta:
        model = Order
        fields = ['owner', 'cart', 'delivery_address',
                  'status', "active", "delivery_fee", "total_amount", "updated_time", "created_time"]

        def create(self, validated_data):
            # Extract the owner and cart data from the validated_data
            owner_data = validated_data.pop('owner')
            cart_data = validated_data.pop('cart')

            # Create the User and Cart objects first
            owner = User.objects.create(**owner_data)
            cart = Cart.objects.create(user=owner, **cart_data)
