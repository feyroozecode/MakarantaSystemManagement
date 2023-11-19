from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone

from apps.corecode.models import StudentClass


class Student(models.Model):
    STATUS_CHOICES = [("active", "Active"), ("inactive", "Inactive")]

    GENDER_CHOICES = [("male", "Garcon"), ("female", "Fille")]

    current_status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="active",
        verbose_name= "Statut Courant"
    )
    registration_number = models.CharField(
        max_length=200, unique=True, verbose_name="Numero d'enregistrement"
    )
    
    surname = models.CharField(max_length=200, verbose_name="Surnom")
    firstname = models.CharField(max_length=200, verbose_name="Nom")
    other_name = models.CharField(max_length=200, blank=True, verbose_name="Dexieme Nom")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default="male", verbose_name="Genre")
    date_of_birth = models.DateField(default=timezone.now, verbose_name="Date de Naissance")
    current_class = models.ForeignKey(
        StudentClass, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Classe actuelle"
    )
    date_of_admission = models.DateField(default=timezone.now, verbose_name="Date d'admission")

    mobile_num_regex = RegexValidator(
        regex="^[0-9]{10,15}$", message="Entered mobile number isn't in a right format!"
    )
    parent_mobile_number = models.CharField(
        validators=[mobile_num_regex], max_length=13, blank=True, verbose_name="Contact parent"
    )

    address = models.TextField(blank=True)
    others = models.TextField(blank=True, verbose_name="Plus de details")
    passport = models.ImageField(blank=True, upload_to="students/passports/", verbose_name="Carte d'identite")

    class Meta:
        ordering = ["surname", "firstname", "other_name"]

    def __str__(self):
        return f"{self.surname} {self.firstname} {self.other_name} ({self.registration_number})"

    def get_absolute_url(self):
        return reverse("student-detail", kwargs={"pk": self.pk})


class StudentBulkUpload(models.Model):
    date_uploaded = models.DateTimeField(auto_now=True)
    csv_file = models.FileField(upload_to="students/bulkupload/")
