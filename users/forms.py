from users.models import Profile
from django import forms
from django.contrib.auth.models import User

faculties=(
    ("1", "IT"),
    ("2", "Civil"),
    ("3", "Computer")   
)

class RegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(max_length=100, widget=forms.PasswordInput)
    faculty=forms.ChoiceField(choices=faculties)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput,
        }

class UserUpdateForm(forms.ModelForm):
    email=forms.EmailField()
    class Meta:
        model=User
        fields=['username','email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['image']
    

