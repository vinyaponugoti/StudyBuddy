from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import logout as log_out
import requests
from studybuddy.models import LutherClass
import json
import urllib
from django.views import generic
from django.utils import timezone

# Create your views here.
# def index(request):
#     return HttpResponse("Study Buddy")

def login(request):
    return render(request,'studybuddy/login.html',{})

def logout(request):
    log_out(request)
    return redirect('/')

def search(request):
    return render(request, 'studybuddy/templates/display_classes.html', {})

class ListOfAllClasses(generic.ListView):
    model = LutherClass
    template_name = 'studybuddy/display_classes.html'
    context_object_name = 'list_of_all_classes'
    def get_queryset(self):
        return LutherClass.objects.all()