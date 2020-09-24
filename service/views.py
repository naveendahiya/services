
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from django.shortcuts import render
from service import models
from rest_framework import viewsets
from service import serializers
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 1000
# Create your views here.

class TaskViewSet(viewsets.ModelViewSet):
    queryset = models.Task.objects.all()
    serializer_class = serializers.TaskSerializers
    pagination_class = StandardResultsSetPagination


class MessageViewSet(viewsets.ModelViewSet):
    queryset = models.Message.objects.all()
    serializer_class = serializers.MessageSerializers


class BidViewSet(viewsets.ModelViewSet):
    queryset = models.Bid.objects.all()
    serializer_class = serializers.BidSerializers
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter,)
    filterset_fields = ('task',)

class LocationViewSet(viewsets.ModelViewSet):
    queryset = models.Location.objects.all()
    serializer_class = serializers.LocationSerializers

class UserViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializers

class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter