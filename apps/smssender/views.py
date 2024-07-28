from django.shortcuts import redirect, render
from django.http import JsonResponse
import requests
from django.contrib import messages
from apps.students.models import Student

from .forms import SMSMessageForm


def send_sms(request):
    base_sms = [
    "Assalam Aleykoum,\nMerci de régler les frais d'inscription et d'avance pour [raison]. Pour toute question, contactez-nous.\nCordialement,\nMéderssa Coranique Imam Malick",
    "Assalam Aleykoum,\nVotre enfant, [nom de l'élève], est exclu temporairement pour [raison]. Veuillez nous contacter.\nCordialement,\nMéderssa Coranique Imam Malick",
    "Assalam Aleykoum,\nNous remarquons des absences fréquentes de votre enfant. Merci de nous contacter.\nCordialement,\nMéderssa Coranique Imam Malick"
]
     
    if request.method == 'POST':
        form = SMSMessageForm(request.POST)
        if form.is_valid():
            # Get the selected students from the form
            selected_students = form.cleaned_data['students']
            message = form.cleaned_data['message']
            
            for student in selected_students:
                parent_phone_number = student.parent_mobile_number
                
                accountId = "AlfajerApps"
                password = "Cohmii5owoow"
                sender = "Imam Malick"

                data = {
                    "accountid": accountId,
                    "password": password,
                    "sender": sender,
                    "to": parent_phone_number,
                    "text": message,
                    "start_date": "",
                    "start_time": "",
                    "stop_time": "",
                    "ret_id": "",
                    "ret_url": "",
                }

                headers = {'Content-Type': 'application/json'}
                
                try:
                    baseURL = "https://lamsms.lafricamobile.com/api"
                    response = requests.post(baseURL, headers=headers, json=data)
                    response.raise_for_status()  # Raise an exception for HTTP errors
                    result = response.json()  # Return the JSON response
                except requests.RequestException as e:
                    # Log the error or handle it as needed
                    return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
                
                if result['status'] == 'error':
                    return JsonResponse({'status': 'error', 'message': result['message']}, status=500)
            
            # Show success message and redirect
            messages.success(request, 'SMS sent successfully!')
            return redirect('send_sms')
    else:
        form = SMSMessageForm()
        
    context = {'form': form, 'base_sms': base_sms}
    return render(request, 'smssender/send_sms.html', context)