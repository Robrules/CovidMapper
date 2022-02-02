from django.http import HttpResponse
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from system.serializers import *
from allauth.account.utils import send_email_confirmation
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


import requests
from datetime import date

def index(request):
    return HttpResponse("Home Page")


@api_view(['POST'])
@permission_classes([IsAuthenticated, ])
def send_verification_email(request):
    send_email_confirmation(request, request.user)
    return Response({"detail": "Verification email sent"})

@api_view(['GET'])
@permission_classes([IsAuthenticated, ])
def getUID(request):
    return Response({"user_id": request.user.id})

@api_view(['GET'])
@permission_classes([IsAuthenticated, ])
def searchLocations(request):
    return Response({"user_id": request.user.id})


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]




class ListViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows lists associated with the logged in user to be viewed or edited.
    """
    serializer_class = ListSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = List.objects.filter(user = self.request.user.id)
        listNameKeyword = self.request.query_params.get('list_name')
        if listNameKeyword:
            queryset = queryset.filter(list_name = listNameKeyword)
        return queryset

class ListLocationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows List-Locations to be viewed or edited.
    """
    serializer_class = ListLocationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = ListLocation.objects.none()
        userLists = List.objects.filter(user = self.request.user.id).values_list('list_id', flat=True)
        list_ids = []
        for p in userLists:
            list_ids.append(int(p))
        for i in list_ids:
            queryset|= ListLocation.objects.filter(list = i)
        listKeyword = self.request.query_params.get('list')
        locationKeyword = self.request.query_params.get('location')
        if listKeyword:
            queryset&= queryset.filter(list = listKeyword)
        if locationKeyword:
            queryset&= queryset.filter(location = locationKeyword)
        return queryset
    

class LocationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows locations to be viewed or edited.
    """
    serializer_class = LocationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Location.objects.all()
        keywords = self.request.query_params.get('street')
        if keywords:
            queryset = queryset.filter(street = keywords)
        return queryset




