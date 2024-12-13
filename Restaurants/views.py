from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .serializers import RestaurantSerializer, DishSerializer, OpeningHourSerializer
from .models import Restaurant, Dish, OpeningHour
from cart.models import Cart
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from cart.serializer import CartSerializer
from .utils import geo


class RestaurantList(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        restaurant = Restaurant.objects.all().prefetch_related('opening_hours_list')
        serializer = RestaurantSerializer(restaurant, many=True)

        return Response(serializer.data)

    def post(self, request):

        rest_address = request.data.get("address")
        lat, lon = geo.geo_address(rest_address)

        user_name = User.objects.get(username=request.user)
        name = request.data.get('name')
        dishes = request.data.get('dishes')
        address = rest_address
        latitude = lat
        longitude = lon
        owner = user_name
        about = request.data.get("about")

        new_rest = Restaurant.objects.create(
            name=name, owner=owner, about=about, address=address, latitude=latitude, longitude=longitude)

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
        rest = restaurant.dishes.get(name=name)
        serializer = DishSerializer(rest)
        return Response(serializer.data)

    def post(self, request, pk, name):
        restaurant = Restaurant.objects.get(pk=pk)

        # dish from the restaurant i want to order from
        dish = restaurant.dishes.get(name=name)

        # details of user ordering
        user = request.user

        # print(user.username)
        if not dish.available:
            return Response({"message": "Dish not available"}, status=status.HTTP_400_BAD_REQUEST)

        # checking if the user has a cart. If he does get it otherwise create a new cart
        print("working")
        try:
            cart, created = Cart.objects.get_or_create(
                user=user)
        except Cart.DoesNotExist:

            return Response({"error": "Unable to create or retrieve cart"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # saving the cart

        # adding a dish to the cart
        if dish not in cart.dishes.all():
            cart.dishes.add(dish)

        cart.save()

        # serializing the cart
        cart_serializer = CartSerializer(cart)
        return Response(cart_serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


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


class nearby_restaurant(APIView):
    def get(self, request):

        address = request.GET.get('address')
        if not address:
            return Response({"error": "Address is required"}, status=status.HTTP_404_NOT_FOUND)
        result = geo.geo_address(address=address)

        Restaurant.objects.filter()

        return Response({"result": result}, status=status.HTTP_200_OK)
