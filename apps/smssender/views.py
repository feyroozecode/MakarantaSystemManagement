from django.shortcuts import render, redirect
from .forms import SMSMessageForm


def send_sms(request):
    if request.method == 'POST':
        form = SMSMessageForm(request.POST)
        if form.is_valid():
            
            # Get the selected student from the form
            selected_student = form.cleaned_data['contact'].student

            # Fetch the parent's phone number
            parent_phone_number = selected_student.parent_mobile_number

            form.save
            
            # send message code..
            
            return redirect('send_sms')
    else :
        form = SMSMessageForm()
        
    #return render(request, 'send_sms', {'form': form})
    return render(request, 'smssender/send_sms.html', {'form': form})