from .models import Restaurant, Dish, OpeningHour
# from django.contrib.auth.models import User
from rest_framework import serializers
from Users import serializers as sr


class OpeningHourSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpeningHour
        fields = ["day", "open_time", "close_time"]


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ['id', 'name', 'photo', 'available']


class RestaurantSerializer(serializers.ModelSerializer):
    opening_hour = OpeningHourSerializer(
        many=True, source='opening_hours_list')
    owner = sr.UserSerializer()
    dishes = DishSerializer(many=True)

    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'about', 'owner',
                  'dishes', 'opening_hour']
