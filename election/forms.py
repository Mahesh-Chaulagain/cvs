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
    username = forms.CharField(disabled=True)
    email = forms.EmailField(disabled=True)
    last_login = forms.CharField(disabled=True)
    password=None
    class Meta:
        model = User
        fields ="__all__"
        exclude = ["password","groups","important dates","is_active","date_joined",] 


class EmailRegistrationForm(forms.ModelForm):
    class Meta:
        model=VerifiedEmail
        fields=['email',]

class ElectionDateForm(forms.ModelForm):
    class Meta:
        model = ElectionDate
        fields = ["result_date"]
        widgets = {
            "result_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

        
        