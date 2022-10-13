from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import logout as log_out
import requests
import json

# Create your views here.
# def index(request):
#     return HttpResponse("Study Buddy")

def login(request):
    return render(request,'studybuddy/login.html',{})

def logout(request):
    log_out(request)
    return redirect('/')

def display_classes(request):
    data = getSISClasses('https://api.devhub.virginia.edu/v1/courses')
    return render(request, 'studybuddy/display_classes.html', {'d': data})

def getSISClasses(url):
    return requests.get(url).json()