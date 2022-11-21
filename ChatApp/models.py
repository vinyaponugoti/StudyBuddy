from django.db import models

# Create your models here.

class ChatRoom(models.Model):
    room_name = models.TextField(blank=True)
    messages_sent = models.IntegerField(blank=True)

    def __str__(self):
        return self.room_name