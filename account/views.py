from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import Film
from .serializers import *
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

# @login_required
# def favorite_add(request, id):
#     film = get_object_or_404(Film, id=id)
#     if film.favorites.filter(id=request.user.id).exists():
#         film.favorites.remove(request.user)
#     else:
#         film.favorites.add(request.user)
#     return HttpResponseRedirect(request.META['HTTP_REFERER'])






class RegisterView(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('Ваш аккаунт успешно зарегистрирован. Вам выслано письмо с кодом активации', status=201)
        return Response(serializer.errors, status=400)


class ActivateView(APIView):
    def post(self, request):
        serializer = ActivationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.activate()
            return Response('Аккаунт успешно активирован')
        return Response(serializer.errors, status=400)


class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        Token.objects.filter(user=user).delete()
        return Response('Вы успешно разлогинились')