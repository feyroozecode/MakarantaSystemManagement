# smssender/forms.py
from django import forms

from apps.students.models import Student

from .models import SMSContact, SMSMessage


class SMSMessageForm(forms.Form):
    students = forms.ModelMultipleChoiceField(
        queryset=Student.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        label='Sélectionnez les étudiants'
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        label='Message personnalisé',
        required=False
    )
    