from django.db import models

# Create your models here.
class LutherClass(models.Model):
    managed = True
    DeptNnemonic = models.CharField(max_length=50)
    DeptName = models.CharField(max_length=50)
    CourseNumber = models.CharField(max_length=50)
    SectionNumber = models.CharField(max_length=50)
    ClassName = models.CharField(max_length=50)
    SectionName = models.CharField(max_length=50)
    ProfessorName = models.CharField(max_length=50)
    ProfessorEmail = models.CharField(max_length=50)
    AvailableSeats = models.CharField(max_length=50)
    DaysOfTheWeek = models.CharField(max_length=50)
    Semester = models.CharField(max_length=50)
    
    def __str__(self):
        return self.DeptNnemonic + self.CourseNumber
    
class Class(models.Model):
    course_mnemonic = models.CharField(max_length=5)
    course_number = models.CharField(max_length=5)
    other_info = models.CharField(max_length=300)

class Mnemonics(models.Model):
    course_mnemonics = models.CharField(max_length=5)


