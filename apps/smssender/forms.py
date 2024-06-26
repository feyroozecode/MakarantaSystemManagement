# smssender/forms.py
from django import forms

from apps.students.models import Student

from .models import SMSContact, SMSMessage


class SMSMessageForm(forms.ModelForm):
    class Meta:
        model = SMSMessage
        fields = ['contact', 'message']

    contact = forms.ModelChoiceField(
        queryset=Student.objects.all(),
        label='Selectionner l\'étudiant',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    
    message = forms.CharField(
        label='Message',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
    )
     