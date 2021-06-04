from django import forms
from .models import Position,Candidate

class PositionForm(forms.ModelForm):
    class Meta:
        model=Position
        fields=('title',)

class CandidateForm(forms.ModelForm):
    class Meta:
        model=Candidate
        fields=('position','name','bio','address','image',)
        
        