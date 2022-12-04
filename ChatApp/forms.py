from cProfile import label
from django import forms

class ChatForm(forms.Form):
    room_name = forms.CharField(label='Create a chat room - enter a name', max_length=100)
