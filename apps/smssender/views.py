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
    
    base_name = ""
    accountId = ""
    password = ""
    sender = ""

    if request.method == 'POST':
        form = SMSMessageForm(request.POST)
        if form.is_valid():
            # Get the selected students from the form
            selected_students = form.cleaned_data['students']
            message = form.cleaned_data['message']
            
            for student in selected_students:
                parent_phone_number = student.parent_mobile_number

                data = {
                    "accountid": accountId,
                    "password": password,
                    "sender": sender,
                    "to": parent_phone_number,
                    "text": message,  #"Salam Aleykoum ce Ibr",
                    # "start_date": "",
                    # "start_time": "",
                    # "stop_time": "",
                    # "ret_id": "",
                    # "ret_url": "",
                }

                headers = {'Content-Type': 'application/json'}
                
                try:
                    baseURL = base_name
                    response = requests.post(baseURL, headers=headers, json=data)
                    print("response", response)
                    print(json.dumps(data, indent=4))
                    response.raise_for_status()  # Raise an exception for HTTP errors
                    result = response.json()  # Return the JSON response
                    print("Response received:", result)
                except requests.RequestException as e:
                    # Log the error or handle it as needed
                    print("Request failed:", str(e))
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

    # if request.method == 'POST':
    #     form = SMSMessageForm(request.POST)
    #     if form.is_valid():
    #         form = SMSMessageForm(request.POST)
    #     if form.is_valid():
    #         # Get the selected student from the form
    #         selected_student_id = form.cleaned_data['student']
    #         selected_student = Student.objects.get(id=selected_student_id)
            
    #         parent_phone_number = selected_student.parent_mobile_number
            
    #         context = {
    #             'parent_phone_number': parent_phone_number,
    #         }
            
    #         selected_students = form.cleaned_data['students']
    #         message = form.cleaned_data['message']

    #         accountId = "AlfajerApps"
    #         password = "Cohmii5owoow"
    #         sender = "Imam Malick"
    #         headers = {'Content-Type': 'application/json'}
    #         baseURL = "https://lamsms.lafricamobile.com/api"

    #         for student in selected_students:
    #             parent_phone_number = student.parent_mobile_number

        
    #             data = {
    #                 "accountid": accountId,
    #                 "password": password,
    #                 "sender": sender,
    #                 "to": parent_phone_number,
    #                 "text": message,
    #                 # "start_date": "",
    #                 # "start_time": "",
    #                 # "stop_time": "",
    #                 # "ret_id": "",
    #                 # "ret_url": "",
    #             }
                
    #             try:
    #                 response = requests.post(baseURL, headers=headers, json=data)
    #                 response.raise_for_status()  # Raise an exception for HTTP errors
    #                 result = response.json()  # Return the JSON response
                    
    #                 print(result)

    #                 if result.get('status') == 'error':
    #                     # If API returns an error, return a JsonResponse with the error message
    #                     return JsonResponse({'status': 'error', 'message': result.get('message', 'Unknown error')}, status=500)
                
    #             except requests.RequestException as e:
    #                 # Log the error or handle it as needed
    #                 return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
                
    #             if result['status'] == 'error':
    #                 return JsonResponse({'status': 'error', 'message': result['message']}, status=500)
            
    #             # Show success message and redirect
    #             messages.success(request, 'SMS sent successfully!')
    #             return redirect('send_sms')
    #     else:
    #         form = SMSMessageForm()
    
    #     context = {'form': form}
    #     return render(request, 'smssender/send_sms.html', context)        
            