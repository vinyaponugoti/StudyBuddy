from dataclasses import fields
from django import forms
from .models import Profile, ScheduleClass
from django.forms import TextInput, EmailInput


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
            "rows": "1",
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
        
        
        