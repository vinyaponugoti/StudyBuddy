from django.urls import path, include
from ChatApp import views as chat_views

app_name = 'chat'

urlpatterns = [
    path("<str:room_name>/", chat_views.room, name='room'),
    path("", chat_views.createChatRoom, name='chat_index'),
    #path("create_room", chat_views.createChatRoom, name='createChatRoom')
]