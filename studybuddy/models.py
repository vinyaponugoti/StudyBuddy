import datetime
from django.db import models
from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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
        return self.DeptNnemonic + str(self.CourseNumber)
    
class Class(models.Model):
    course_mnemonic = models.CharField(max_length=5)
    course_number = models.CharField(max_length=5)
    other_info = models.CharField(max_length=300)

class Mnemonics(models.Model):
    course_mnemonics = models.CharField(max_length=5)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, blank=True)
    email = models.EmailField(max_length = 254, blank=True)
    year = models.CharField(max_length=100, blank=True)
    major = models.TextField(blank=True)
    interests = models.TextField(blank=True)
    classes = models.ManyToMany(LutherClass)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User) 
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    

@receiver(post_save, sender=User) 
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()



