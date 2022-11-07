from dataclasses import fields
from django import forms
from .models import Profile, StudyPost
from django.forms import TextInput, EmailInput
from django.forms import ModelForm


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['user'].widget.attrs.update({
            'hidden' : 'hidden'
        })
        self.fields['major'].widget.attrs.update({
            "rows": "1"
        })
        self.fields['interests'].widget.attrs.update({
            "rows": "5"
        })
    class Meta: 
        model = Profile
        fields = "__all__"
		# fields = ('name','email','year','major','interests','classes','friends_list')
        
# making a studypost form
class StudyPostForm(ModelForm):
    class Meta:
        model = StudyPost
        fields = ('user', 'groupUsers', 'location', 'studyClass', 'description', 'timeDate')
        #'user', 'groupUsers', 'timeDate', 'location', 'studyClass', 'requests', 'description'
        hidden_fields = 'user'

        labels = {
            'groupUsers': 'Other Studies Buddies Joining:',
            'location': '',
            'studyClass': 'Pick the class your session will focus on:',
            'description': '',
            'timeDate': "Pick your study session's date and time",
            'user': ''
        }

        widgets = {
            'user': forms.HiddenInput(attrs={'class': 'form-control'}),
            'groupUsers': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Describe your study location'}),
            'studyClass': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Describe yourself and your plans for the study session'}),
            'timeDate': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'})
        }