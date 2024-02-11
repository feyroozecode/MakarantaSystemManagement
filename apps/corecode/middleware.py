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

from apps.corecode.models import AcademicSession
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseServerError

class SiteWideConfigs:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            # Get the current session if it exists
            current_session = AcademicSession.objects.get(current=True)
        except ObjectDoesNotExist:
            # If AcademicSession with current=True does not exist, attempt to create a new one
            try:
                # Set any existing session with current=True to current=False
                AcademicSession.objects.filter(current=True).update(current=False)
                # Create a new default session
                current_session = AcademicSession.objects.create(
                    name="Default Session",
                    start_date="2024-01-01",
                    end_date="2024-12-31",
                    current=True
                )
            except Exception as e:
                # If an error occurs during creation, handle it and return a server error response
                print("Error creating AcademicSession:", e)
                return HttpResponseServerError("Internal Server Error")

        # Assign the current_session to the request object
        request.current_session = current_session

        # Pass the request to the next middleware or view
        response = self.get_response(request)

        return response
