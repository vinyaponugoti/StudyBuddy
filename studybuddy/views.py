from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout as log_out
import requests
from studybuddy.models import LutherClass
import json
import urllib
from django.views import generic
from django.utils import timezone
from .forms import ProfileForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from .models import Profile, FriendRequest, StudyPost
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import StudyPostForm

# Create your views here.
# def index(request):
#     return HttpResponse("Study Buddy")

def login(request):
    return render(request,'studybuddy/login.html',{})

def logout(request):
    log_out(request)
    return redirect('/')

@login_required(login_url='loginrequired')
def search(request):
    return render(request, 'studybuddy/display_classes.html', {})

@login_required(login_url='loginrequired')
def profile(request):
    profile_data = Profile.objects.get(user=request.user.id)
    request_list = FriendRequest.objects.all().filter(requested=request.user.profile, is_accepted=False)
    friend_list = Profile.get_friends_list(request.user)

    context = {
        "profile_data": profile_data,
        "request_list": request_list,
        "friend_list": friend_list,
    }
    return render(request,'studybuddy/profile.html',context)

@login_required(login_url='loginrequired')
def uploadStudyPost(request):
    profile_data = Profile.objects.get(user=request.user.id)
    user_classes = Profile.getClasses(request.user.profile)
    user_friends = Profile.get_friends_list(request.user.profile)

    initial_data = {
        'user': profile_data
    }
    form = StudyPostForm(initial=initial_data)
    submitted = False
    if request.method == "POST":
        form = StudyPostForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/upload?submitted=True')
    else:
        form = StudyPostForm
        if 'submitted' in request.GET:
            submitted = True
    context = {
        "user_classes" : user_classes,
        "user_friends" : user_friends,
        "form" : form,
        "submitted" : submitted
    }
    return render(request, 'studybuddy/upload.html', context)

@login_required(login_url='loginrequired')
def home(request):
    profile_data = Profile.objects.get(user=request.user.id)
    user_friends = Profile.get_friends_list(request.user.profile)
    friends_posts = []
    for friend in user_friends:
        friends_posts.append(Profile.objects.get(user=friend.user.id))
    context = {
        "friends_posts": friends_posts
    }
    return render(request, 'studybuddy/home.html', context)

class ListOfAllClasses(generic.ListView):
    model = LutherClass
    template_name = 'studybuddy/display_classes.html'
    context_object_name = 'list_of_all_classes'
    def get_queryset(self):
        return LutherClass.objects.all()


class UpdateProfile(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    form_class = ProfileForm
    login_url = "loginrequired"
    template_name = "studybuddy/editprofile.html"
    success_url = reverse_lazy("profile")
    
    def get_object(self):
        return self.request.user.profile

@login_required(login_url='loginrequired')
def view_requests(request):
    # list of pending friend request sent to user
    request_list = FriendRequest.objects.all().filter(requested=request.user.profile, is_accepted=False)
   
    # list of profiles who requested the user
    request_senders = []
    for r in request_list:
        request_senders.append(r.requester)
            
    # number of profiles that requested the user    
    request_num = len(request_senders)

    context = {
        "request_list": request_list,
        "request_senders": request_senders,
        "request_num": request_num,
    }
    return render(request,'studybuddy/friends.html',context)

# Clean this up!!
@login_required(login_url='loginrequired')
def view_all_profiles(request):
    # All profiles
    profiles_list = Profile.objects.all().exclude(user=request.user)

    # The og user's profile
    og_profile = Profile.objects.get(user=request.user.id)

    # Friend Requests for the user
    # Requests sent to the user
    requests_by = FriendRequest.objects.filter(requested=request.user.profile)
    # Requests sent by the user (variable names are switched on purpose)
    requests_for= FriendRequest.objects.filter(requester=request.user.profile)

    # Contains the profiles of the users who sent the requests to the user
    requests_by_user = []
    for r in requests_by:
        requests_by_user.append(r.requester)

    # Contains the profiles of the users who the current user sent the request to
    requests_for_user = []
    for r in requests_for:
        requests_for_user.append(r.requested)

    # Getting list of profiles that user can send requests to
    requests_to_and_from_og = FriendRequest.objects.filter(Q(requester=og_profile) | Q(requested=og_profile))
    # Og user can't send requests to these profiles
    cant_send_requests_to = []
    for r in requests_to_and_from_og:
        if r.is_accepted == True:
            cant_send_requests_to.append(r.requester)
            cant_send_requests_to.append(r.requested)
    # Og user can send requests to these profiles
    can_send_requests_to = []
    for p in profiles_list:
        if p not in cant_send_requests_to:
            can_send_requests_to.append(p)

    context = {
        "profiles_list": profiles_list,
        "can_send_requests_to": can_send_requests_to,
        "requests_by_user": requests_by_user,
        "requests_for_user": requests_for_user,
        "requests_by": requests_by,
        "requests_for": requests_for,
    }
    return render(request,'studybuddy/allprofiles.html',context)

@login_required(login_url='loginrequired')
def click_add_friend(request):
    if request.method == "POST":
        primary_key = request.POST.get('primary_key_profile')
        user = request.user
        requester = Profile.objects.get(user=user)
        requested = Profile.objects.get(pk=primary_key)
        friend_req = FriendRequest.objects.create(requester=requester, requested = requested, is_accepted=False)

    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

@login_required(login_url='loginrequired')
def click_remove_friend(request):
    if request.method == "POST":
        primary_key = request.POST.get('primary_key_profile')
        user = request.user
        requester = Profile.objects.get(user=user)
        requested = Profile.objects.get(pk=primary_key)
        friend_req = (FriendRequest.objects.filter(requester=requester) & FriendRequest.objects.filter(requested=requested)) | (FriendRequest.objects.filter(requester=requested) & FriendRequest.objects.filter(requested=requester))
        friend_req.delete()

    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

@login_required(login_url='loginrequired')
def accept_request(request):
    if request.method == "POST":
        primary_key = request.POST.get('primary_key_profile')
        user = request.user
        requester = Profile.objects.get(pk=primary_key)
        requested = Profile.objects.get(user=user)
        friend_req = get_object_or_404(FriendRequest,requester=requester,requested=requested)
        if friend_req.is_accepted == False:
            friend_req.is_accepted = True
            friend_req.save()

        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

@login_required(login_url='loginrequired')
def decline_request(request):
    if request.method == "POST":
        primary_key = request.POST.get('primary_key_profile')
        user = request.user
        requester = Profile.objects.get(pk=primary_key)
        requested = Profile.objects.get(user=user)
        friend_req = get_object_or_404(FriendRequest,requester=requester,requested=requested)
        friend_req.delete()

        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

@login_required(login_url='loginrequired')
def view_profile(request, username):
        profiles_list = Profile.objects.all().exclude(user=request.user)
        user_list = User.objects.all()
        user_match = None
        for u in user_list:
            if(u.username == username):
                user_match = u
        
        profile_data = Profile.objects.get(user=user_match)

        
        context = {
            "profiles_list":profiles_list,
            "profile_data":profile_data,
            "user":user_match,
        }
        
        return render(request,'studybuddy/profile.html',context)

def loginrequired(request):
    return render(request, 'studybuddy/loginrequired.html')