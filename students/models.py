from django.db import models
from django.utils import timezone
from django.urls import reverse

from corecode.models import StudentClass

class Student(models.Model):
  STATUS = [
      ('active', 'Active'),
      ('inactive', 'Inactive')
  ]

  GENDER = [
      ('male', 'Male'),
      ('female', 'Female')
  ]

  current_status = models.CharField(
      max_length=10, choices=STATUS, default='active')
  registration_number = models.CharField(max_length=200, unique=True)
  surname = models.CharField(max_length=200)
  firstname = models.CharField(max_length=200)
  other_name = models.CharField(max_length=200, blank=True)
  gender = models.CharField(max_length=10, choices=GENDER, default='male')
  date_of_birth = models.DateField(default=timezone.now)
  current_class = models.ForeignKey(
      StudentClass, on_delete=models.SET_NULL, blank=True, null=True)
  date_of_admission = models.DateField(default=timezone.now)
  parent_mobile_number = models.CharField(max_length=15, blank=True)
  address = models.TextField(blank=True)
  others = models.TextField(blank=True)

  class Meta:
    ordering = ['registration_number']

  def __str__(self):
    return f'{self.surname} {self.firstname} {self.other_name} ({self.registration_number})'

  def get_absolute_url(self):
    return reverse('student-detail', kwargs={'pk': self.pk})


class StudentBulkUpload(models.Model):
  date_uploaded = models.DateTimeField(auto_now=True)
  csv_file = models.FileField(upload_to='bulkupload/student/')
  current_class = models.ForeignKey(StudentClass, on_delete=models.CASCADE)