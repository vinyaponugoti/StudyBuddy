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

def updateClasses():
    class_mnemonic = requests.get('http://luthers-list.herokuapp.com/api/deptlist?format=json').json()
    #print(class_mnumonic)
    last_dm = ''
    last_cn = ''
    for cm in class_mnemonic:
        data = requests.get('http://luthers-list.herokuapp.com/api/dept/' + cm['subject'] + '?format=json').json()
        for each in data:
            if not(last_dm == each['subject'] and last_cn == each['catalog_number']):
                last_dm = each['subject']
                last_cn = each['catalog_number']
                try:
                    if LutherClass.objects.filter(CourseNumber = each['course_number']).exists():
                        model = LutherClass.objects.filter(CourseNumber = each['course_number'])[0]
                    else:
                        model = LutherClass()
                    model.DeptNnemonic = each['subject']
                    model.CourseNumber = each['course_number']
                    model.CatalogNumber = each['catalog_number']
                    model.SectionNumber = each['course_section']
                    model.ClassName = each['description']
                    model.ProfessorName = each['instructor']['name']
                    model.ProfessorEmail = each['instructor']['email']
                    model.AvailableSeats = each['class_capacity']
                    #model.DaysOfTheWeek = each['meetings'][0]['days']
                    model.Semester = each['semester_code']
                    #print("Updated " + model)
                    model.save()
                except:
                    pass

class ListOfAllClasses(generic.ListView):
    #updateClasses()
    model = LutherClass
    template_name = 'studybuddy/display_classes.html'
    context_object_name = 'list_of_all_classes'
    def get_queryset(self):
        return LutherClass.objects.all()