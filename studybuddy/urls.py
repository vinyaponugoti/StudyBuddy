from django.urls import path

from . import views
from ChatApp import views as chat_views

handler404 = views.view_404 

urlpatterns = [
    # path('', views.index, name='index'),
    path('home', views.home, name='home'),
    path('', views.login, name='login'),
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
    path('studyposts/<str:lutherClassName>', views.view_classes,name="viewclass"),
    path('studyposts/<str:lutherClassName>/postsnotjoined', views.view_classes_notjoined,name="postsnotjoined"),
    path('loginrequired', views.loginrequired, name='loginrequired'),
    path('editschedule', views.add_class, name='schedule'),
    # path('editschedule',views.UpdateSchedule.as_view(), name = 'editschedule'),,
    path('loginrequired', views.loginrequired, name='loginrequired'),
    # path('upload', views.uploadStudyPost, name='uploadStudyPost'),
    path('sessions/<str:class_name>', views.view_session, name='viewsessions'),
    # path('createpost',views.add_study_post,name='createpost'),
    path('upload', views.add_study_post, name='uploadStudyPost'),
    # path('uploadclassesfirst', views.are_no_classes, name='uploadclassesfirst'),
    path('studyposts',views.view_study_posts, name="studyposts"),
    path('studypostslatest',views.view_latest_study_posts,name="latestsessions"),
    path('studypostsearliest',views.view_earliest_study_posts,name="earliestsessions"),
    path('studypostsnames',views.view_class_order_study_posts,name="studypostsnames"),
    path('yourposts',views.view_your_posts, name="yourposts"),
    path("attendingposts",views.view_all_attending_posts,name="attendingposts"),
    path("friendsposts",views.view_friends_posts,name="friendsposts"),
    path('viewpostrequests',views.view_post_requests,name="viewpostrequests"),
    path('joinsession',views.click_join_session, name='joinsession'),
    path('acceptrequest',views.accept_post_request, name='acceptrequest'),
    path('declinerequest',views.decline_post_request, name='declinerequest'),
    path('leavesession',views.click_leave_session, name='leavesession'),
    path('deletepost',views.delete_post, name='deletepost'),
    path('planner', views.planner, name='planner'),
    path('chat', chat_views.createChatRoom, name='chat_index'),
    path('closepost', views.closepost, name='closepost'),
    path('deleteclass',views.delete_class, name='deleteclass'),
    
]