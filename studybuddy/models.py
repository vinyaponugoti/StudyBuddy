from django.db import models

# Create your models here.
class SISClass(models.Model):
    deptDict = {"CS" : "Computer Science"}
    
    DeptNnemonic = models.TextField()
    DeptName = models.TextField()
    CourseNumber = models.IntegerField()
    SectionNumber = models.IntegerField()
    ClassName = models.TextField()
    SectionName = models.TextField()
    ProfessorName = models.TextField()
    AvailableSeats = models.IntegerField()
    DaysOfTheWeek = models.TextField()
    Semester = models.TextField()
    
    def __str__(self):
        return self.title
class Class(models.Model):
    course_mnemonic = models.CharField(max_length=5)
    course_number = models.CharField(max_length=5)
    other_info = models.CharField(max_length=300)

class Mnemonics(models.Model):
    course_mnemonics = models.CharField(max_length=5)


