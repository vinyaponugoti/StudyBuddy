"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('studybuddy.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('logout/', include('studybuddy.urls')),
    path('search/', include('studybuddy.urls')),
    path("chat", include("ChatApp.urls")),
    path("profile/", include('studybuddy.urls')),
    path("editprofile/", include('studybuddy.urls')),
    path("profile/<str:username>", include('studybuddy.urls')),
    path('requests/',include('studybuddy.urls')),
    path('allprofiles/',include('studybuddy.urls')),
    path('addfriend/',include('studybuddy.urls')),
    path('removefriend/',include('studybuddy.urls')),
    path('acceptfriend/',include('studybuddy.urls')),
    path('declinefriend/',include('studybuddy.urls')),
]