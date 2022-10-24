from django.urls import path

from . import views


urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.login, name='login'),
    path('logout',views.logout, name='logout'),
    path('studybuddy/classes',views.ListOfAllClasses.as_view(), name='classes'),
    path('search', views.search, name='search'),
    path('editprofile',views.UpdateProfile.as_view(), name = 'editprofile'),
    path('profile',views.profile, name='profile')
]