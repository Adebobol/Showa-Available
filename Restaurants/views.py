from django.shortcuts import render
from rest_framework.views import APIView, Response
from .models import Restaurant
from .serializers import RestaurantSerializer
# Create your views here.


class RestaurantList(APIView):
    def get(self, request):
        restaurants = Restaurant.objects.all()
        serializer = RestaurantSerializer(restaurants, many=True)

        return Response(serializer.data)
