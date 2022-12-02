from sqlite3 import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout as log_out
import requests
from studybuddy.models import LutherClass, StudySession, StudyPost, PostRequest
import json
import urllib
from django.views import generic
from django.utils import timezone
from .forms import ProfileForm, ScheduleForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from .models import Profile, FriendRequest, ScheduleClass
from .forms import ScheduleNewPost
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator


def login(request):
    return render(request,'studybuddy/home.html', {})

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

    # Adding Schedule to Profile
    schedule = Profile.get_classes(request.user.profile)

    # Number of Friends user has
    friends_num = len(friend_list)

    # Getting the number of Friend Requests the user has
    request_list = FriendRequest.objects.all().filter(requested=request.user.profile, is_accepted=False)
    request_num = len(request_list)

    context = {
        "profile_data": profile_data,
        "request_list": request_list,
        "friend_list": friend_list,
        "schedule": schedule,
        "friends_num": friends_num,
        "request_num": request_num,
    }
    return render(request,'studybuddy/profile.html',context)

@login_required(login_url='loginrequired')
def home(request):
    profile_data = Profile.objects.get(user=request.user.id)
    user_friends = Profile.get_friends_list(request.user.profile)
    friends_posts = []
    friends_num = len(user_friends)

    for friend in user_friends:
        # friends_posts.append(Profile.objects.get(user=friend.user.id))
        friends_posts.append(Profile.get_friends_list(request.user.profile))

    context = {
        "profile_data" : profile_data,
        "friends_posts": friends_posts,
        "friends_num": friends_num,
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

@login_required(login_url='loginrequired')
def view_classes(request, lutherClassName):
    other_posts = StudyPost.objects.all().exclude(user=request.user)

    # List of posts that the user is able to send post requests to
    can_request = []

    for p in other_posts:
        can_request.append(p)

    for p in StudyPost.objects.all().exclude(user=request.user):
        for g in p.groupUsers.all():
            if g == request.user:
                can_request.remove(p)

    for r in PostRequest.objects.all().filter(is_accepted=False):
        if r.buddy == request.user.profile:
            can_request.remove(r.studyposting)

    len_p = len(can_request)

    # List of posts that the user has sent requests to
    post_pending = []
    for r in PostRequest.objects.all().filter(is_accepted=False):
        if r.buddy == request.user.profile:
            post_pending.append(r.studyposting)

    # List of posts that the user created
    user_posts = []
    for p in StudyPost.objects.all():
        if p.user == request.user:
            if p.session == False:
                user_posts.append(p)

    # List of posts that the user is a member of (not owner)
    member_posts = []
    for p in StudyPost.objects.all().exclude(user=request.user):
        for g in p.groupUsers.all():
            if g == request.user:
                member_posts.append(p)

    class_list = []

    
    for u in StudyPost.objects.all():
        if u.user_luther_class.ClassName == lutherClassName:
            class_list.append(u)

    classes_num = len(class_list)
    
    # p = Paginator(class_list, 4)
    # page_number = request.GET.get('page', 1)

    # try:
    #     page = p.page(page_number)
    # except:
    #     page = p.page(1)

    context = {
        "posts": class_list,
        "can_request": can_request,
        "len_p": len_p,
        "post_pending": post_pending,
        "user_posts": user_posts,
        "member_posts": member_posts,
        "class_post_title": lutherClassName,
        "classes_num": classes_num,
        "class_list":class_list,
    }
    return render(request, 'studybuddy/classposts.html', context)

@login_required(login_url='login_required')
def view_sessions(request, class_name):
    #this will return a list of all the study sessions
    if class_name == 'all':
        return render(request, 'studybuddy/study_session_list.html', {"session_list": StudyPost.objects.all(),
                                                "course": 'all'})

    study_sessions = StudyPost.objects.all()
    study_sessions_for_class = list()
    study_session_course = None



    #if class_name != 'all', we will look for study_session posts of the same class.
    for session in study_sessions:
        course = session.user_luther_class
        course_name = course.DeptNnemonic + str(course.CatalogNumber) + ": " + course.ClassName
        if course_name == class_name:
            study_sessions_for_class.append(session)
            study_session_course = course

    context = {
        "session_list": study_sessions_for_class,
        "course": study_session_course
    }

    return(request, '/studybuddy/study_session_list.html', context)


def view_class(request, class_name):
    print(class_name)
    class_list = LutherClass.objects.all()
    course_match = None
    for course in class_list:
        if str(course) == class_name:
            course_match = course
    course_obj = StudySession.objects.get(course=course_match)
    
    context = {
        "course_study_sessions": course_obj,
        
    }
    return render(request, 'studybuddy/login.html', context)

def view_session(request, class_name, date):
    class_list = LutherClass.objects.all()
    course_match = None
    for course in class_list:
        if str(course) == class_name:
            course_match = course

    course_obj = StudySession.objects.get(course=course_match, day = date)
    
    context = {
        "course_study_sessions": course_obj
    }
    return render(request, 'studybuddy/home.html', context)

def loginrequired(request):
    return render(request, 'studybuddy/loginrequired.html')


def add_class(request):
    if request.method == "POST":
        form = ScheduleForm(request.POST)
        if form.is_valid():
            schedule_form = form.save(commit=False)
            schedule_form.classes_owner = request.user
            schedule_form.save()
        else:
            messages.error(request, "Error saving class")

        return redirect("schedule")
    schedule_form = ScheduleForm()
    classes = ScheduleClass.objects.all()

    try:
        luther_list = []
        for c in classes:
            error = 0
            if c.classes_owner == request.user:
                if not LutherClass.objects.filter(Q(DeptNnemonic=c.class_department) & Q(CatalogNumber=c.class_number)):
                    # messages.error(request,"Error: This class doesn't exist \nMake sure department and number are entered correctly")
                    error = 1
                    pass
                else:
                    luther_list.append(LutherClass.objects.filter(
                        Q(DeptNnemonic=c.class_department) & Q(CatalogNumber=c.class_number))[0])
                    error = 0
    except IndexError:
        messages.error(request, "Error: Class Number is too high or too low")

    if error == 1:
        messages.error(request,
                       "Error: Class does not exist. Make sure class department and class number are entered correctly")

    current_profile = Profile.objects.get(user=request.user)
    current_profile.classes.set(luther_list)

    # Use this when getting user's classes in other views
    updated_classes = Profile.get_classes(request.user.profile)

    context = {
        "schedule_form": schedule_form,
        "classes": classes,
        "luther_list": luther_list,
        "updated_classes": updated_classes,
    }

    return render(request, 'studybuddy/schedule.html', context)


@login_required(login_url='loginrequired')
def add_study_post(request):
   
    no_classes = False
    schedule = Profile.get_classes(request.user.profile)
    if len(schedule) == 0 :
        no_classes = True

    if request.method == "POST":
        form = ScheduleNewPost(request.POST, user=request.user)

        if form.is_valid():
            form.instance.user = request.user
            # form.instance.user_class = classes[0]
            form.save()
        else:
            messages.error(request, "Error saving post")

        # return redirect("uploadStudyPost")
        return redirect("studyposts")

    else:
         form = ScheduleNewPost(user=request.user)

    form = ScheduleNewPost(user=request.user)
    posts = StudyPost.objects.all()
    updated_classes = Profile.get_classes(request.user.profile)

    

    context= {
        "form":form,
        "posts":posts,
        "updated_classes":updated_classes,
        "no_classes": no_classes,
    }

    return render(request,'studybuddy/upload.html',context)

# def are_no_classes(request):
#     no_classes = False

#     schedule = Profile.get_classes(request.user.profile)
#     if len(schedule) == 0 :
#         no_classes = True

#     context = {
#         "no_classes": no_classes,
#     }

#     return render(request,'studybuddy/upload.html',context)


def view_study_posts(request):
    posts = StudyPost.objects.all()

    other_posts = StudyPost.objects.all().exclude(user=request.user)
    
    # List of posts that the user is able to send post requests to
    can_request = []

    for p in other_posts:
        can_request.append(p)

    for p in StudyPost.objects.all().exclude(user=request.user):
        for g in p.groupUsers.all():
            if g == request.user:
                can_request.remove(p)

    for r in PostRequest.objects.all().filter(is_accepted=False):
        if r.buddy == request.user.profile:
            can_request.remove(r.studyposting)


    len_p = len(can_request)


    # List of posts that the user has sent requests to
    post_pending = []
    for r in PostRequest.objects.all().filter(is_accepted=False):
        if r.buddy == request.user.profile:
            post_pending.append(r.studyposting)

    # List of posts that the user created
    user_posts = []
    for p in StudyPost.objects.all():
        if p.user == request.user:
            if p.session == False:
                user_posts.append(p)

    # List of posts that the user is a member of (not owner)
    member_posts = []
    for p in StudyPost.objects.all().exclude(user=request.user):
        for g in p.groupUsers.all():
            if g == request.user:
                member_posts.append(p)


    p = Paginator(posts,4)
    page_number = request.GET.get('page',1)
    

    try:
        page = p.page(page_number)
    except:
        page = p.page(1)

    context={
        "posts":posts,
        "can_request":can_request,
        "len_p": len_p,
        "post_pending":  post_pending,
        "user_posts": user_posts,
        "member_posts":member_posts,
        "page":page,
        "class_post_title": "All",
    }
    return render(request, 'studybuddy/posts.html', context)

@login_required(login_url='loginrequired')
def planner(request):
    studysessions = []

    userposts = StudyPost.objects.filter(user=request.user)
    sessions = userposts.exclude(session=False)
    for s in sessions:
        studysessions.append(s)

    for p in StudyPost.objects.all().exclude(user=request.user):
        if p.session == True:
            for g in p.groupUsers.all():
                if g == request.user:
                    studysessions.append(p)

    context = {
        "studysessions" : studysessions
    }

    return render(request,'studybuddy/planner.html', context)

@login_required(login_url='loginrequired')
def view_post_requests(request):
    # list of pending post requests sent to post
    post = StudyPost.objects.all().filter(user=request.user)

    request_list = []
    for sp in PostRequest.objects.all().filter(is_accepted=False):
        for p in post:
            if p == sp.studyposting:
                request_list.append(sp)

   
    # # list of profiles who requested the post
    request_senders = []
    for r in request_list:
        request_senders.append(r.buddy)
            
    # number of profiles that requested the user    
    request_num = len(request_senders)

    context = {
        "request_list": request_list,
        "request_senders": request_senders,
        "request_num": request_num,
    }
    return render(request,'studybuddy/postrequests.html',context)


@login_required(login_url='loginrequired')
def click_join_session(request):
    if request.method == "POST":
        primary_key = request.POST.get('primary_key_post')
        user = request.user
        requester = Profile.objects.get(user=user)
        posting = StudyPost.objects.get(pk=primary_key)
        post_req = PostRequest.objects.create(buddy=requester, studyposting = posting, is_accepted=False)

    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


@login_required(login_url='loginrequired')
def click_leave_session(request):
    if request.method == "POST":
        try:
            primary_key = request.POST.get('primary_key_post')
            user = request.user
            requester = Profile.objects.get(user=user)
            requested = StudyPost.objects.get(pk=primary_key)
            post_req = get_object_or_404(PostRequest,buddy=requester,studyposting=requested)
            post_req.delete()
        except:
            primary_key = request.POST.get('primary_key_post')
            user = request.user
            posting = StudyPost.objects.get(pk=primary_key)
            posting.groupUsers.remove(user)

    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


@login_required(login_url='loginrequired')
def accept_post_request(request):
    if request.method == "POST":
        primary_key = request.POST.get('primary_key_posts')
        user = request.user
        requester = PostRequest.objects.get(pk=primary_key).buddy
        requested = PostRequest.objects.get(pk=primary_key).studyposting
        post_req = get_object_or_404(PostRequest,buddy=requester,studyposting=requested)
        if post_req.is_accepted == False:
            post_req.is_accepted = True
            post_req.save()

        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


@login_required(login_url='loginrequired')
def decline_post_request(request):
    if request.method == "POST":
        primary_key = request.POST.get('primary_key_post')
        user = request.user
        requester = PostRequest.objects.get(pk=primary_key).buddy
        requested = PostRequest.objects.get(pk=primary_key).studyposting
        post_req = get_object_or_404(PostRequest,buddy=requester,studyposting=requested)
        post_req.delete()

        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


@login_required(login_url='loginrequired')
def delete_post(request):
    if request.method == "POST":
        primary_key = request.POST.get('primary_key_post')
        study_post = StudyPost.objects.get(pk=primary_key)
        study_post.delete()

        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

@login_required(login_url='loginrequired')
def closepost(request):
    if request.method == "POST":
        primary_key = request.POST.get('primary_key_post')
        study_post = StudyPost.objects.get(pk=primary_key)
        study_post.session = True
        study_post.save()

        #return render(request, 'studybuddy/planner.html')
        return HttpResponseRedirect('/planner')



@login_required(login_url='loginrequired')
def delete_class(request):
    if request.method == "POST":
        primary_key = request.POST.get('primary_key_post')
        class_to_delete = Profile.objects.get(user=request.user.id).classes.get(pk=primary_key)
        # class_to_delete.delete()
        class_dep = class_to_delete.DeptNnemonic
        class_num = class_to_delete.CatalogNumber
        # print(class_to_delete)
        # print(class_dep)
        # print(class_num)
        classes = ScheduleClass.objects.all().filter(class_department=class_dep, class_number=class_num, classes_owner=request.user)
        for c in classes:
            c.delete()

        Profile.objects.get(user=request.user.id).classes.remove(class_to_delete)
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


def view_404(request, exception=None):
    # make a redirect to homepage
    # you can use the name of url or just the plain link
    return redirect('/') # or redirect('name-of-index-url')