from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm

class PositionForm(forms.ModelForm):
    class Meta:
        model=Position
        fields=('title',)

class CandidateForm(forms.ModelForm):
    class Meta:
        model=Candidate
        fields=('position','name','bio','address','image',)

class CustomUserChangeForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields ="__all__"
        exclude = ["password","last login","groups","important dates",] 


class EmailRegistrationForm(forms.ModelForm):
    class Meta:
        model=VerifiedEmail
        fields=['email',]

        
        