
from django.db import models

from django import forms
from .models import User

class UserForm(forms.ModelForm ):
        name=forms.CharField(max_length=30)  
        number = forms.NumberInput() # validators should be a list
        password=forms.CharField(widget=forms.PasswordInput)
        class Meta:
                model = User
                fields="__all__"