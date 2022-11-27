from django.db import models
import django
from django.contrib.auth.models import User

# Create your models here.

class ChatRoom(models.Model):
    room_name = models.TextField(blank=True)
    messages_sent = models.IntegerField(blank=True)

    def __str__(self):
        return self.room_name

class Chat(models.Model):
    content = models.CharField(max_length=1000)
    timestamp = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey('ChatRoom', on_delete=models.CASCADE)