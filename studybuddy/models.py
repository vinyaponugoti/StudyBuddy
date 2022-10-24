import datetime
from django.db import models
from django.utils import timezone
from django.contrib import admin
# Create your models here.
class LutherClass(models.Model):    
    DeptNnemonic = models.TextField()
    DeptName = models.TextField()
    CourseNumber = models.IntegerField()
    CatalogNumber = models.IntegerField(default = 0)
    SectionNumber = models.IntegerField()
    ClassName = models.TextField()
    SectionName = models.TextField()
    ProfessorName = models.TextField()
    ProfessorEmail = models.TextField()
    AvailableSeats = models.IntegerField()
    DaysOfTheWeek = models.TextField()
    Semester = models.TextField()
    
    def __str__(self):
        return self.DeptNnemonic + self.CourseNumber
    
class Class(models.Model):
    course_mnemonic = models.CharField(max_length=5)
    course_number = models.CharField(max_length=5)
    other_info = models.CharField(max_length=300)

class Mnemonics(models.Model):
    course_mnemonics = models.CharField(max_length=5)


