from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Cart
from .serializer import CartSerializer


@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def cart_detail(request):
    if request.method == "GET":
        cart = Cart.objects.get(user=request.user)
        cart_serializer = CartSerializer(cart)

        return Response(cart_serializer.data)
