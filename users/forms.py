from django.forms import fields
from django.forms.widgets import EmailInput
from users.models import *
from django import forms
from django.contrib.auth.models import User

class RegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(max_length=100, widget=forms.PasswordInput)
    first_name=forms.CharField(max_length=20,required=True)
    last_name=forms.CharField(max_length=20,required=True)
    email=forms.EmailField(required=True)
    image=forms.ImageField()
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput,
        }

class UserUpdateForm(forms.ModelForm):
    email=forms.EmailField(disabled=True)
    class Meta:
        model=User
        fields=['username','email','first_name','last_name']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['image']
    

