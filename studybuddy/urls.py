from django.urls import path

from . import views


urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.home, name='home'),
    path('login', views.login, name='login'),
    path('logout',views.logout, name='logout'),
    path('classes',views.ListOfAllClasses.as_view(), name='classes'),
    path('search', views.search, name='search'),
    path('editprofile',views.UpdateProfile.as_view(), name = 'editprofile'),
    path('profile',views.profile, name='profile'),
    path('requests',views.view_requests, name='requests'),
    path('allprofiles',views.view_all_profiles, name='allprofiles'),
    path('addfriend',views.click_add_friend, name='addfriend'),
    path('removefriend',views.click_remove_friend, name='removefriend'),
    path('acceptfriend',views.accept_request, name='acceptfriend'),
    path('declinefriend',views.decline_request, name='declinefriend'),
    path('profile/<str:username>',views.view_profile,name="viewprofile"),
    path('loginrequired', views.loginrequired, name='loginrequired'),
    path('editschedule', views.add_class, name='schedule'),
    # path('editschedule',views.UpdateSchedule.as_view(), name = 'editschedule'),,
    path('loginrequired', views.loginrequired, name='loginrequired'),
    path('upload', views.uploadStudyPost, name='uploadStudyPost'),
    path('<str:class_name>', views.view_class, name='viewclass'),
    path('sessions/<str:date>', views.view_session, name='viewsessions')
]