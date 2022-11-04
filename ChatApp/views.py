from django.shortcuts import render, redirect
 
 
def room(request, room_name):
    return render(request, 'ChatApp/room.html', {'room_name': room_name})

def index(request):
    if not request.user.is_authenticated:
        return redirect("login")
    context = {}
    return render(request, 'ChatApp/index.html')