from django.contrib import admin
from .models import LutherClass, Profile, FriendRequest,  ScheduleClass
# Register your models here.

admin.site.register(LutherClass)
admin.site.register(Profile)
admin.site.register(FriendRequest)
admin.site.register(ScheduleClass)
# admin.site.register(Schedule)

