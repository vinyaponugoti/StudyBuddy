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

def updateClasses():
    class_mnemonic = requests.get('http://luthers-list.herokuapp.com/api/deptlist?format=json').json()
    #print(class_mnumonic)
    for cm in class_mnemonic:
        data = requests.get('http://luthers-list.herokuapp.com/api/dept/' + cm['subject'] + '?format=json').json()
        for each in data:
            model = LutherClass()
            model.DeptNnemonic = each['subject']
            model.CourseNumber = each['course_number']
            model.SectionNumber = each['course_section']
            model.ClassName = each['description']
            model.ProfessorName = each['instructor']['name']
            model.ProfessorEmail = each['instructor']['email']
            model.AvailableSeats = each['class_capacity']
            #model.DaysOfTheWeek = each['meetings'][0]['days']
            model.Semester = each['semester_code']
            #print(model)
            model.save()
class ListOfAllClasses(generic.ListView):
    #updateClasses()
    model = LutherClass
    template_name = 'studybuddy/display_classes.html'
    context_object_name = 'list_of_all_classes'
    def get_queryset(self):
        return LutherClass.objects.all()