# smssender/forms.py
from django import forms
from .models import SMSMessage, SMSContact
from apps.students.models import Student

class SMSMessageForm(forms.ModelForm):
    class Meta:
        model = SMSMessage
        fields = ['contact', 'message']

    contact = forms.ModelChoiceField(
        queryset=Student.objects.all(),
        label='Selectionner l\'étudiant',
        widget=forms.Select(attrs={'class': 'form-control'}),
       
    )
    