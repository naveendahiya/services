from rest_framework import serializers
from service import models

class TaskSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Task
        fields = "__all__"

class MessageSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Message
        fields = "__all__"

class LocationSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Location
        fields = "__all__"

class BidSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Bid
        fields = "__all__"

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = '__all__'