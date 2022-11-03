from dataclasses import fields
from django import forms
from .models import Profile
from django.forms import TextInput, EmailInput


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
        
        