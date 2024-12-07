# forms.py
from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['section', 'name', 'firstname', 'arabic_name', 'gender', 'nationality',
                 'date_of_birth', 'birth_city', 'current_class', 'date_of_admission',
                 'parent_mobile_number', 'second_parent_mobile_number', 'has_learned_quran',
                 'health_state', 'health_type', 'passport', 'address', 'others', 'current_status']
        exclude = ['registration_number']
        widgets = {
            'section': forms.Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 100%; font-size: 1.1em;'
            }),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'date_of_admission': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'section': 'Section de l\'étudiant',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make section field required and prominent
        self.fields['section'].required = True
        self.fields['section'].widget.attrs['class'] = 'form-control select2 form-control-lg'
        # Set the register_number field as read-only
        self.fields['registration_number'].widget.attrs['readonly'] = True