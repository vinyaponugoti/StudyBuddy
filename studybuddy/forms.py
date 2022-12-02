from dataclasses import fields
from django import forms
from .models import Profile, ScheduleClass, StudyPost, LutherClass
from django.forms import TextInput, EmailInput
from django.forms import ModelForm
from django.contrib.auth.models import User


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self.fields['user'].widget.attrs.update({
        #     'hidden' : 'hidden'
        # })
        self.fields['major'].widget.attrs.update({
            "rows": "1"
        })
        self.fields['interests'].widget.attrs.update({
            "rows": "5"
        })
        # self.fields['friends_list'].widget.attrs.update({
        #     'hidden' : 'hidden'
        # })
    class Meta: 
        model = Profile
        fields = ('name','email','year','major','interests')
        # fields = "__all__"


class ScheduleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['class_department'].widget.attrs.update({
            "rows": "2",
            "required": True,
            "placeholder": "Enter department abbreviation all uppercase (Ex. For class CS 1110 enter CS) ",
        })

        self.fields['class_number'].widget.attrs.update({
            "rows": "1",
            "required": True,
            "placeholder": "Enter class catalog number (Ex. For class CS 1110 enter 1110)"
        })

    class Meta: 
        model = ScheduleClass
        fields = ('class_department','class_number')

        




# making a studypost form
# class StudyPostForm(ModelForm):
#     class Meta:
#         model = StudyPost
#         fields = ('groupUsers', 'location', 'studyClass', 'description', 'timeDate')
#         #'user', 'groupUsers', 'timeDate', 'location', 'studyClass', 'requests', 'description'
#         hidden_fields = 'user'

#         labels = {
#             'groupUsers': 'Other Studies Buddies Joining:',
#             'location': '',
#             'studyClass': 'Pick the class your session will focus on:',
#             'description': '',
#             'timeDate': "Pick your study session's date and time"
#             #'user': ''
#         }

#         widgets = {
#             'groupUsers': forms.SelectMultiple(attrs={'class': 'form-control', 'style': 'max-width: 600px;'}),
#             'location': forms.TextInput(attrs={'class': 'form-control', 'style': 'max-width: 600px;', 'placeholder': 'Describe your study location'}),
#             'studyClass': forms.SelectMultiple(attrs={'class': 'form-control', 'style': 'max-width: 600px;'}),
#             'description': forms.TextInput(attrs={'class': 'form-control', 'style': 'max-width: 600px;', 'placeholder':'Describe yourself and your plans for the study session'}),
#             'timeDate': forms.DateTimeInput(attrs={'class': 'form-control', 'style': 'max-width: 600px;', 'type': 'datetime-local'})
#         }





# Form that lets users create study posts

class ScheduleNewPost(forms.ModelForm):
    def __init__(self, *args, **kwargs):
            user = kwargs.pop('user','')
            super(ScheduleNewPost, self).__init__(*args, **kwargs)

            

            self.fields['user_luther_class']=forms.ModelChoiceField(
                queryset=Profile.get_classes(user.profile), 
                widget=forms.Select(attrs={'class': 'form-control', 'style': 'max-width: 600px;'}),
                label= 'Pick the class your session will focus on:',
                )


            self.fields["groupUsers"] = forms.ModelMultipleChoiceField(
                # queryset=User.objects.all().exclude(username=user.username).order_by('username'),
                queryset=Profile.get_friends_list(user.profile),
                widget=forms.SelectMultiple(attrs={'class': 'form-control', 'style': 'max-width: 600px;',}),
                label = "Select Any of Your Friends that are joining ",
                required = False
            )

            if len(Profile.get_friends_list(user.profile)) == 0 :
                self.fields['groupUsers'].widget.attrs.update({
                    'hidden' : 'hidden'
                })

    class Meta: 
        model = StudyPost
        fields = ('user_luther_class', "timeDate","location","groupUsers","description")

        labels = {
            'groupUsers': 'Other Study Buddies Joining',
            'location': '',
            'description': '',
            'timeDate': "Pick your study session's date and time"
        }

        widgets = {
            'location': forms.TextInput(attrs={'class': 'form-control', 'style': 'max-width: 600px;', 'placeholder': 'Describe your study location'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'style': 'max-width: 600px;', 'placeholder':'Describe yourself and your plans for the study session'}),
            'timeDate': forms.DateTimeInput(attrs={'class': 'form-control', 'format': '%d/%m/%Y %H:%M', 'style': 'max-width: 600px;', 'type': 'datetime-local'}),
        }

    


       
        
