from django.shortcuts import render
from service import models
from rest_framework import viewsets
from service import serializers
# Create your views here.

class TaskViewSet(viewsets.ModelViewSet):
    queryset = models.Task.objects.all()
    serializer_class = serializers.TaskSerializers

class BidViewSet(viewsets.ModelViewSet):
    queryset = models.Bid.objects.all()
    serializer_class = serializers.BidSerializers

class LocationViewSet(viewsets.ModelViewSet):
    queryset = models.Location.objects.all()
    serializer_class = serializers.LocationSerializers

class UserViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializers