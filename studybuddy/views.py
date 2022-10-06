from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import logout as log_out

# Create your views here.
# def index(request):
#     return HttpResponse("Study Buddy")

def login(request):
    return render(request,'studybuddy/login.html',{})

def logout(request):
    log_out(request)
    return redirect('/')