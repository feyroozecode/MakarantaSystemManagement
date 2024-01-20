from django.shortcuts import render, redirect
from .forms import SMSMessageForm

from apps.students.models import Student

def send_sms(request):
    if request.method == 'POST':
        form = SMSMessageForm(request.POST)
        if form.is_valid():
            
            # Get the selected student from the form
            selected_student_id = form.cleaned_data['student']
            selected_student = Student.objects.get(id=selected_student_id)
            
            #
            parent_phone_number = selected_student.parent_mobile_number
            
            context = {
                'parent_phone_number': parent_phone_number,
            }
            
            form.save
            
            return redirect('send_sms')
    else :
        form = SMSMessageForm()
        
    context = {'form': form}
    return render(request, 'smssender/send_sms.html', context)