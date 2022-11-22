from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ChatRoom(models.Model):
    room_name = models.TextField(blank=True)
    messages_sent = models.IntegerField(blank=True)

    def __str__(self):
        return self.room_name\
            
class Message(models.Model):
    author = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    context = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)