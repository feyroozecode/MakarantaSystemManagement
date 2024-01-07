
from django.urls import path
from apps.corecode.urls import urlpatterns
from .views import send_sms

urlpatterns = [
    path('send-sms/', send_sms, name='send-sms'),
]
