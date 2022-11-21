from django.shortcuts import render, redirect
from django.views import generic
from .models import ChatRoom
from django.http import HttpResponse, HttpResponseRedirect
from .forms import ChatForm
 
 
def room(request, room_name):
    if ChatRoom.objects.filter(room_name = room_name).exists():
        return render(request, 'ChatApp/room.html', {'room_name': room_name})
    else:
        return redirect("chat_index")
    
def createChatRoom(request):
    # if this is a POST request we need to process the form data
    if not request.user.is_authenticated:
        return redirect("login")
    model = ChatRoom()
    template_name = 'ChatApp/index.html'
    rooms = ChatRoom.objects.all()
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ChatForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            if not ChatRoom.objects.filter(room_name = form.data['room_name']).exists():
                model = ChatRoom()
                model.room_name = form.data['room_name']
                model.messages_sent = 0
                model.save()
            return HttpResponseRedirect(form.data['room_name'])

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ChatForm()

    return render(request, 'ChatApp/index.html', {'form': form, 'rooms' : rooms})