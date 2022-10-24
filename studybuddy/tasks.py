from __future__ import absolute_import, unicode_literals
from celery import task
from .models import LutherClass
import requests


@task()
def updateClassesDB():
    class_mnemonic = requests.get('http://luthers-list.herokuapp.com/api/deptlist?format=json').json()
    #print(class_mnumonic)
    last_dm = ''
    count = 0
    last_cn = ''
    for cm in class_mnemonic:
        data = requests.get('http://luthers-list.herokuapp.com/api/dept/' + cm['subject'] + '?format=json').json()
        for each in data:
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
                count +=1
            except:
                pass
    #print(count)