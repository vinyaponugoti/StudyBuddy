from django.urls import path

from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.login, name='login'),
    path('logout',views.logout, name='logout'),
    path('classes',views.ListOfAllClasses.as_view(), name='classes')
]