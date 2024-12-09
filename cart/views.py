from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
# Create your views here.


@api_view(['GET', 'POST'])
def Cart_detail(request):
    return
