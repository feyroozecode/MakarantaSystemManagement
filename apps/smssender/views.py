from django.shortcuts import redirect, render
from django.http import JsonResponse
import requests
from django.contrib import messages
from apps.students.models import Student
import json

from .forms import SMSMessageForm

def send_sms(request):

    base_sms = [
        "Assalam Aleykoum,Merci de régler les frais d'inscription et d'avance pour [raison]. Pour toute question, contactez-nous. Cordialement, Méderssa Coranique Imam Malick",
        "Assalam Aleykoum, Votre enfant, [nom de l'élève], est exclu temporairement pour [raison]. Veuillez nous contacter. Cordialement, Méderssa Coranique Imam Malick",
        "Assalam Aleykoum, Nous remarquons des absences fréquentes de votre enfant. Merci de nous contacter.Cordialement,Méderssa Coranique Imam Malick"
    ]

    # Ensure these variables are set correctly
    base_name = "https://lamsms.lafricamobile.com/api"  # Set your base URL
    accountId = "AlfajerApps"  # Set your account ID
    password = "Cohmii5owoow"  # Set your password
    sender = "Imam Malick"  # Set your sender name

    if request.method == 'POST':
        form = SMSMessageForm(request.POST)
        if form.is_valid():
            selected_students = form.cleaned_data['students']
            message = form.cleaned_data['message']
            
            for student in selected_students:
                parent_phone_number = student.parent_mobile_number

                data = {
                    "accountid": accountId,
                    "password": password,
                    "sender": sender,
                    "to": parent_phone_number,
                    "text": message,
                }

                headers = {'Content-Type': 'application/json'}
                
                try:
                    response = requests.post(base_name, headers=headers, json=data)
                    response.raise_for_status()  # Raise an exception for HTTP errors
                    result = response.json()  # Return the JSON response
                    
                    # Check if the API response indicates success
                    if result.get('status') == 'error':
                        return JsonResponse({'status': 'error', 'message': result.get('message', 'Unknown error')}, status=500)
                except requests.RequestException as e:
                    print("Request failed:", str(e))  # Log the error
                    return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
            
            messages.success(request, 'SMS sent successfully!')
            return redirect('send_sms')
    else:
        form = SMSMessageForm()
        
    context = {'form': form, 'base_sms': base_sms}
    return render(request, 'smssender/send_sms.html', context)