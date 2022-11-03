from django.contrib import admin
from .models import LutherClass, Profile, FriendRequest
# Register your models here.

admin.site.register(LutherClass)
admin.site.register(Profile)
admin.site.register(FriendRequest)
