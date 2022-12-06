from django.db import models
from django.utils import timezone
import datetime
from datetime import date
from django.contrib import admin
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.core.exceptions import ValidationError
import uuid

# Create your models here.

def validate_year(value):
    try:
        converted_value = int(value)
    except:
        raise ValidationError("Please enter a valid graduation year (ex. 2023)")

    if converted_value < 2023:
        raise ValidationError("Only current students are allowed")
    elif converted_value > 2026:
        raise ValidationError("Only current students are allowed")


def validate_study_post_date(value):
    # curr_time = datetime.datetime.now()
    curr_time = date.today()

    # if value.date < curr_time:
    if value.date() < curr_time:
        raise ValidationError("You cannot set the session date to a time in the past")

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
        return self.DeptNnemonic + str(self.CatalogNumber) + ": " + self.ClassName
    def get_deptname(self):
        return self.DeptNnemonic
    def get_coursenumber(self):
        return self.CourseNumber
        
class ScheduleClass(models.Model):
    class_department = models.TextField(blank=True)
    class_number = models.IntegerField(blank=True)
    classes_owner = models.ForeignKey(User,on_delete=models.CASCADE, related_name="classes_owner", default=1)

    def __str__(self):
        return f"{self.class_department} {self.class_number}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, blank=True)
    email = models.EmailField(max_length = 254, blank=True)
    year = models.CharField(max_length=100, blank=True, validators=[validate_year])
    major = models.TextField(blank=True)
    interests = models.TextField(blank=True)
    classes = models.ManyToManyField(LutherClass)
    friends_list = models.ManyToManyField(User, blank=True, related_name="friends_list")

    def get_friends_list(self):
        return self.friends_list.all()
    def getClasses(self):
        return self.classes.all()




    def get_classes(self):
        return self.classes.all()

    def __str__(self):
        return self.user.username

class Class(models.Model):
    course_mnemonic = models.CharField(max_length=5)
    course_number = models.CharField(max_length=5)
    other_info = models.CharField(max_length=300)

@receiver(post_save, sender=User) 
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    

@receiver(post_save, sender=User) 
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class StudyPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    user_luther_class = models.ForeignKey(LutherClass, on_delete=models.CASCADE, default=1, related_name="user_luther_class")
    groupUsers = models.ManyToManyField(User, related_name="other_users_joining", blank=True)
    timeDate = models.DateTimeField(default=timezone.now, blank=True, validators=[validate_study_post_date])
    location = models.CharField(max_length=200, blank=True)
    # studyClass = models.ManyToManyField(ScheduleClass,blank=True)
    requests = models.ManyToManyField(User, related_name = "users_want_to_join", blank=True)
    description = models.TextField(max_length=500, default="", blank=True)
    session = models.BooleanField(default=False)
    # user_class = models.ForeignKey(ScheduleClass, on_delete=models.CASCADE, default=1, related_name="user_class")
    

    def __str__(self):
        return f"{self.user} wants to study at {self.location} at {self.timeDate} for {self.user_luther_class} with {self.groupUsers.all()}"

    def get_studiers_list(self):
        return self.groupUsers.all()

class StudySession(models.Model):
    day = models.DateField()
    course = models.OneToOneField(LutherClass,
                                  on_delete=models.CASCADE)
    students = models.ManyToManyField(Profile)

    def __str__(self):
        return self.day + ' - ' + self.course

    def get_students(self):
        return self.students.all()

    def get_dates(self):
        return self.day.all()

    def add_student(self, User):
        self.students.add(User)


class FriendRequest(models.Model):
    requester = models.ForeignKey(Profile,on_delete=models.CASCADE, related_name="requester")
    requested = models.ForeignKey(Profile,on_delete=models.CASCADE, related_name="requested")
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.requester} wants to be friends with {self.requested}"

@receiver(post_save,sender=FriendRequest)
def post_save_mutuals(sender, instance, created, **kwargs):
    requester_user = instance.requester
    requested_user = instance.requested
    if instance.is_accepted == True:
        requester_user.friends_list.add(requested_user.user)
        requested_user.friends_list.add(requester_user.user)
        requester_user.save()
        requested_user.save()

@receiver(pre_delete,sender=FriendRequest)
def pre_delete_removing_friends(sender, instance, **kwargs):
    requester_user = instance.requester
    requested_user = instance.requested
    requester_user.friends_list.remove(requested_user.user)
    requested_user.friends_list.remove(requester_user.user)
    requester_user.save()
    requested_user.save()



class PostRequest(models.Model):
    buddy = models.ForeignKey(Profile,on_delete=models.CASCADE, related_name="buddy")
    studyposting = models.ForeignKey(StudyPost,on_delete=models.CASCADE, related_name="studypost")
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.buddy} wants to join {self.studyposting}"

@receiver(post_save,sender=PostRequest)
def post_save_member(sender, instance, created, **kwargs):
    buddy = instance.buddy
    studyposting = instance.studyposting
    if instance.is_accepted == True:
        studyposting.groupUsers.add(buddy.user)
        studyposting.save()
        buddy.save()

@receiver(pre_delete,sender=PostRequest)
def pre_delete_removing_member(sender, instance, **kwargs):
    buddy = instance.buddy
    studyposting = instance.studyposting
    studyposting.groupUsers.remove(buddy.user)
    studyposting.save()
    buddy.save()


