from dataclasses import fields
from django import forms
from .models import Profile
from django.forms import TextInput, EmailInput


class ProfileForm(forms.ModelForm):
    class Meta: 
        model = Profile
        fields = "__all__"
		# fields = ('name','email','year','major','interests')
        
        widgets = {
            'name': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Name'
                }),
            'email': EmailInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 300px;',
                'placeholder': 'Email'
                }),
            'year': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Year'
                }),
            'major': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Major'
                }),
            'interests': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Interests'
                }),
        }