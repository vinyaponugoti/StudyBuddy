from django.urls import path, include
from ChatApp import views as chat_views

urlpatterns = [
    path("", chat_views.chatPage, name="chat-page"),
]