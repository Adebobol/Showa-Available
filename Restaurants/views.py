from rest_framework.views import APIView
from .serializers import RestaurantSerializer, DishSerializer
from .models import Restaurant, Dish
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt


class RestaurantList(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        restaurant = Restaurant.objects.all().prefetch_related('opening_hours_list')
        serializer = RestaurantSerializer(restaurant, many=True)

        return Response(serializer.data)

    def post(self, request):

        user_name = User.objects.get(username=request.user)
        name = request.data.get('name')
        dishes = request.data.get('dishes')
        owner = user_name
        about = request.data.get("about")

        new_rest = Restaurant.objects.create(
            name=name, owner=owner, about=about)

        serializer = RestaurantSerializer(new_rest)

        return Response(serializer.data)


class RestaurantDetail(APIView):

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_restaurant(self, pk):
        try:
            restaurant = Restaurant.objects.get(pk=pk)
            return restaurant
        except Restaurant.DoesNotExist:
            raise Http404

    def get(self, request, pk):

        restaurant = self.get_restaurant(pk)
        serializer = RestaurantSerializer(restaurant)
        return Response(serializer.data)

    def put(self, request, pk):
        if request.user == Restaurant.objects.get(pk=pk).owner:
            # user = Restaurant.objects.get(pk=pk).owner
            restaurant = self.get_restaurant(pk)
            serializer = RestaurantSerializer(restaurant, data=request.data)

            if serializer.is_valid():
                serializer.save()

                return Response(serializer.data)

    def delete(self, request, pk):
        if request.user == Restaurant.objects.get(pk=pk).owner:

            restaurant = self.get_restaurant(pk)
            restaurant.delete()

            return Response({"message": "Restaurant deleted..."})


class DishList(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_restaurant(self, pk):
        try:
            restaurant = Restaurant.objects.get(pk=pk)
            return restaurant
        except Restaurant.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        restaurant = self.get_restaurant(pk)
        dishes = restaurant.dishes.all()
        serializer = DishSerializer(dishes, many=True)

        return Response(serializer.data)

    def post(self, request, pk):
        restaurant = self.get_restaurant(pk=pk)

        name = request.data.get("name")
        photo = request.FILES.get("photo")
        available = request.data.get("available")
        dish_data = {
            "name": name,
            "photo": photo,
            "available": available
        }

        dish_serializer = DishSerializer(data=dish_data)
        if dish_serializer.is_valid():
            sr_dish = dish_serializer.save()
            restaurant.dishes.add(sr_dish)
            return Response(dish_serializer.data, status=status.HTTP_201_CREATED)
        return Response(dish_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DishDetail(APIView):

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, name):
        restaurant = Restaurant.objects.get(pk=pk)
        rest = restaurant.dishes.filter(name=name)
        serializer = DishSerializer(rest, many=True)
        return Response(serializer.data)
