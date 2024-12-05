from .models import Restaurant, Dish
# from django.contrib.auth.models import User
from rest_framework import serializers
from Users import serializers as sr


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ['id', 'name', 'photo', 'available']


class RestaurantSerializer(serializers.ModelSerializer):

    owner = sr.UserSerializer()
    dishes = DishSerializer(many=True)

    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'about', 'owner', 'dishes']
