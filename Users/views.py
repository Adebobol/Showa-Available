from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .forms import UserRegisterForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
import json
# Create your views here.


@csrf_exempt
# @api_view(['GET', 'POST'])
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        confirm_password = data.get("confirm_password")

        # checking if user exists
        if_user = User.objects.filter(username=username)
        if if_user.exists():
            return JsonResponse({"User already exist."})

        if password != confirm_password:
            return JsonResponse({"Password don't match."})

        else:
            user = User.objects.create(username=username, email=email,
                                       password=password)
            user.set_password(password)
            user.save()
            login_user = authenticate(username=username, password=password)
            if login_user is not None:
                login(request, login_user)

                return JsonResponse({
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'message': 'User created successfully'
                }, status=201)
    return JsonResponse({'error': "Wrong Request"}, status=405)
