
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from django.shortcuts import render
from rest_framework.decorators import action
from service import models
from rest_framework import viewsets
from service import serializers
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse,Http404
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

    @action(methods=['get',], detail=True, url_path="location", url_name="location")
    def get_location(self, request, pk):
        try:
            location = models.Location.objects.get(task = pk)
        except models.Location.DoesNotExist:
            return Response({'empty': 'No location is avaliable for this task'},  status=status.HTTP_204_NO_CONTENT)
        serialized = serializers.LocationSerializers(location)
        return Response(serialized.data)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = models.Message.objects.all()
    serializer_class = serializers.MessageSerializers


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = models.Question.objects.all()
    serializer_class = serializers.QuestionSerializers


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = models.Answer.objects.all()
    serializer_class = serializers.AnswerSerializers


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