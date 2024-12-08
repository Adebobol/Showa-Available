from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .serializers import RestaurantSerializer, DishSerializer, OpeningHourSerializer
from .models import Restaurant, Dish, OpeningHour
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


class Opening_hours_restaurant(APIView):

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_restaurant(self, pk):
        try:
            restaurant = Restaurant.objects.get(pk=pk)
            return restaurant
        except Restaurant.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        restaurant = self.get_restaurant(pk=pk)
        opening_hour = restaurant.opening_hours_list.all()
        serializer = OpeningHourSerializer(opening_hour, many=True)
        return Response(serializer.data)

    @csrf_exempt
    def post(self, request, pk):
        restaurant = self.get_restaurant(pk=pk)

        day = request.data.get("day")
        open_time = request.data.get("open_time")
        close_time = request.data.get("close_time")

        particular_day = {
            # "restaurant": restaurant.pk,
            "day": day,
            "open_time": open_time,
            "close_time": close_time
        }

        opening_hour_serializer = OpeningHourSerializer(data=particular_day)

        if opening_hour_serializer.is_valid():
            new_opening_hour = opening_hour_serializer.save(
                restaurant=restaurant)
            restaurant.opening_hours_list.add(new_opening_hour)
            return Response(opening_hour_serializer.data, status=status.HTTP_201_CREATED)
        return Response(opening_hour_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def restaurant_order(request):
    pass
