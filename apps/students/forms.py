# forms.py
from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        # Exclude register_number field as it's auto-generated
        exclude = ['registration_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set the register_number field as read-only
        self.fields['registration_number'].widget.attrs['readonly'] = True