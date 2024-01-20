from django.db import models
from apps.students.models import Student

class SMSContact(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    
    
class SMSMessage(models.Model):
    contact = models.ForeignKey(SMSContact, on_delete=models.CASCADE)
    message = models.TextField()