from django.urls import path, include
from ChatApp import views as chat_views

urlpatterns = [
    path("<str:room_name>/", chat_views.room, name='room'),
    path("", chat_views.index, name='index'),
]