#from .models import AcademicSession, AcademicTerm


#class SiteWideConfigs:
#    def __init__(self, get_response):
#        self.get_response = get_response

#    def __call__(self, request):
#        current_session = AcademicSession.objects.get(current=True)
#        current_term = AcademicTerm.objects.get(current=True)

#        request.current_session = current_session
#        request.current_term = current_term

#        response = self.get_response(request)

#        return response

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseServerError

class SiteWideConfigs:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            current_session = AcademicSession.objects.get(current=True)
        except ObjectDoesNotExist:
            # Create a new AcademicSession or show an error message
            try:
                # Attempt to create a new AcademicSession with default values
                current_session = AcademicSession.objects.create(
                    # Provide default values for the AcademicSession fields
                    # Adjust these values according to your application's requirements
                    name="Default Session",
                    start_date="2024-01-01",
                    end_date="2024-12-31",
                    current=True
                )
            except Exception as e:
                # If an error occurs while creating the AcademicSession, handle it here
                # For example, log the error and return a server error response
                print("Error creating AcademicSession:", e)
                return HttpResponseServerError("Internal Server Error")

        request.current_session = current_session

        response = self.get_response(request)

        return response
