from django.contrib.auth.models import User, Group
from rest_framework import serializers
from system.models import *

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class ListSerializer(serializers.ModelSerializer):
    class Meta():
        model = List
        fields = ['list_name', 'list_id', 'user']

class ListLocationSerializer(serializers.ModelSerializer):
    class Meta():
        model = ListLocation
        fields = ['list', 'location']
    

class LocationSerializer(serializers.ModelSerializer):
    class Meta():
        model = Location
        fields = ['location_id', 'street']
