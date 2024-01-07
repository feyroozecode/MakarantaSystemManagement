# smssender/forms.py
from django import forms
from .models import SMSMessage, SMSContact

class SMSMessageForm(forms.ModelForm):
    class Meta:
        model = SMSMessage
        fields = ['contact', 'message']

    contact = forms.ModelChoiceField(
        queryset=SMSContact.objects.all(),
        label='Select contact',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )