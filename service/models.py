from django.db import models
from django.core.validators import MinLengthValidator
import datetime
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    mobile = models.IntegerField(null=True)


class Task(models.Model):
    description = models.CharField(max_length=500, validators=[MinLengthValidator(10)])
    price = models.FloatField()
    title = models.CharField(max_length=50, validators=[MinLengthValidator(5)])
    due_date = models.DateTimeField()
    STATUS_CHOICES = [
        ("O", "Open"),
        ("C", "Close")
    ]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='O')
    selected = models.IntegerField(default=-1)

    creater = models.ForeignKey(User, related_name='mytasks', on_delete=models.CASCADE)


class Location(models.Model):
    address = models.CharField(max_length=500, validators=[MinLengthValidator(10)])
    latitude = models.FloatField()
    longitude = models.FloatField()
    pincode = models.IntegerField(default=0)

    task = models.ForeignKey(Task, related_name='location', on_delete=models.CASCADE)


class Bid(models.Model):
    comment = models.CharField(max_length=500, validators=[MinLengthValidator(10)])
    offer = models.FloatField()

    task = models.ForeignKey(Task, related_name='bids', on_delete=models.CASCADE)
    creater = models.ForeignKey(User, related_name='mybids', on_delete=models.CASCADE)


class Message(models.Model):
    message = models.CharField(max_length=1024, null=False)
    timestamp = datetime.datetime.now()

    creater = models.ForeignKey(User, related_name='mymessage', on_delete=models.CASCADE)
    task = models.ForeignKey(Task, related_name='task_chat', on_delete=models.CASCADE)


class Question(models.Model):
    question = models.CharField(max_length=500, null=False)
    timestamp = datetime.datetime.now()

    creater = models.ForeignKey(User, related_name='myquestions', on_delete=models.CASCADE)
    task = models.ForeignKey(Task, related_name='task_questions', on_delete=models.CASCADE)


class Answer(models.Model):
    answer = models.CharField(max_length=500, null=False)
    timestamp = datetime.datetime.now()

    creater = models.ForeignKey(User, related_name='myanswers', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='questionanswer', on_delete=models.CASCADE)



