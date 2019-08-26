from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.authentication import TokenAuthentication, BasicAuthentication

from .models import UserStatus, GPSCoordinates
from .viewHelper import createUser, login, validateUser, getCoordinates

from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)

@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny,))
def CreateUserView(request):
    if request.method == 'POST':
        print("Create user")
        username = request.data.get("username")
        password = request.data.get("password")
        output = validateUser(username, password)
        if output is True:
            return createUser(username, password)
        return output
    return Response("Check request method", status = status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny,))
def UserLoginView(request):
    print("Login view")
    if request.method == 'POST':
        username = request.data.get("username")
        password = request.data.get("password")
        output = validateUser(username, password)
        print(output)
        if output is True :
           return login(username, password)
        return output
    return Response("Check request method", status = status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['POST'])
@authentication_classes((TokenAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def UserStatusView(request):
       
    if request.method == 'POST':
        user_status = request.data['status']
        user = request.user.username
        userstatus = UserStatus.objects.filter(username=user).first()
        userstatus.status = user_status
        userstatus.save()
        return Response("Ok", status = status.HTTP_200_OK)

@csrf_exempt
@api_view(['GET', 'POST'])
@authentication_classes((TokenAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def CoordinatesView(request):
    if request.method == 'POST':
        userstatus = UserStatus.objects.filter(username = request.user.username).first()
        if request.data.get('longitude') and request.data.get('latitude') and request.data.get('altitude'):
            coordinates = GPSCoordinates.objects.create(userstatus_gps = userstatus)
            coordinates.longitude = request.data.get('longitude')
            coordinates.latitude = request.data.get('latitude')
            coordinates.altitude = request.data.get('altitude')
            coordinates.save()
            return Response("Ok", status = status.HTTP_201_CREATED)
        
        return Response("Check your json", status = status.HTTP_400_BAD_REQUEST)
    
    # Request latest coordinates
    if request.method == 'GET':
        userstatus = UserStatus.objects.filter(username=request.user.username).first()
        query = {}
        queryList = []
        if userstatus:
            # find user coordinates
            return getCoordinates(userstatus)
            
        
                

