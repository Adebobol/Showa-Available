from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Cart
from .serializer import CartSerializer, OrderSerializer
from django.http import JsonResponse
import json
from django.http import Http404
from Users.serializers import UserSerializer
from django.contrib.auth.models import User


@api_view(['GET', 'POST', 'PUT'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def cart_detail_get(request):
    if request.method == "GET":
        cart = Cart.objects.get(user=request.user)
        cart_serializer = CartSerializer(cart)

        return Response(cart_serializer.data)

    dish_id = request.data.get("dish_id")
    if request.method == "PUT":
        cart = Cart.objects.get(user=request.user)
        about_to = cart.dishes.get(id=dish_id)
        if about_to is not None:

            cart.dishes.remove(about_to)
            cart_serializer = CartSerializer(cart)
            return Response(cart_serializer.data)
        return Response({"message": "Dish no longer in order"})


@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def cart_checkout(request):

    # if request.method == "POST":
    #     ur_sr = UserSerializer(request.user)
    #     cart = Cart.objects.get(user=request.user)
    #     cr_sr = CartSerializer(cart)

    #     owner = ur_sr.data
    #     cart = cr_sr.data
    #     delivery_address = request.data.get("delivery_address")

    #     order_data = {
    #         "cart": cart,
    #         "owner": owner,
    #         "delivery_address": delivery_address,
    #     }

    #     order_serializer = OrderSerializer(data=order_data)
    #     if order_serializer.is_valid():
    #         order_serializer.save()
    #         return Response({"message": "valid order"})
    #     else:
    #         return Response(order_serializer.errors, status=400)

    if request.method == "POST":
        try:
            ur_sr = UserSerializer(request.user)
            cart = Cart.objects.get(user=request.user)
            cr_sr = CartSerializer(cart)
        except Cart.DoesNotExist:
            return Response({"error": "Cart not found for this user."}, status=404)

        owner = request.user.id
        cart_data = cr_sr.data
        delivery_address = request.data.get("delivery_address")

        if not delivery_address:
            return Response({"error": "Delivery address is required."}, status=400)

        # Handle photo fields properly, ensure the files are sent correctly in the request
        for dish in cart_data.get("dishes", []):
            if 'photo' in dish and isinstance(dish['photo'], str):
                return Response({"error": "Photo field must be a file."}, status=400)

        order_data = {
            "cart": cart.id,
            "owner": owner,
            "delivery_address": delivery_address,
        }

        order_serializer = OrderSerializer(data=order_data)
        if order_serializer.is_valid():
            order = order_serializer.save()
            return Response({"message": "Order placed successfully", "order_id": order.id})
        else:
            return Response(order_serializer.errors, status=400)

    if request.method == 'GET':
        user = request.user
        cart = Cart.objects.get(user=user)

        cart_sr = CartSerializer(cart)
        return Response(cart_sr.data)
