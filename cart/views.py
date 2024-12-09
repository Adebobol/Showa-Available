from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Cart
from .serializer import CartSerializer
from django.http import JsonResponse


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
            return Response(cart)
        return Response({"message": "Dish no longer in order"})


@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def cart_checkout(request):
    pass
