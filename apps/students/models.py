from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone

from apps.corecode.models import StudentClass
from django.urls import reverse_lazy
#from apps.students.utils import generate_student_number


class Student(models.Model):
    STATUS_CHOICES = [("active", "Active"), ("inactive", "Inactive")]

    GENDER_CHOICES = [("male", "Garcon"), ("female", "Fille")]
    
    CITYES_CHOICE = [("niamey", "Niamey"), ("agadez", "Agadez"), ("diffa", "Diffa"), ("dosso", "Dosso"), ("maradi", "Maradi"), ("tahoua", "Tahoua"), ("tillaberi", "Tillaberi"), ("zinder", "Zinder") ]

    HAS_LEARNED_QURAN = [('yes', "Oui"), ('no', "Non")] 
    
    HEALTH_STATE_CHOICES = [("healthy", "Sain"), ("unhealthy", "Malade")]

    mobile_num_regex = RegexValidator(
        regex="^[0-9]{10,15}$", message="Entered mobile number isn't in a right format!"
    )
     
    current_status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="active",
        verbose_name= "Statut Courant"
    )
    registration_number = models.CharField(
        max_length=10,
        unique=True,
        #default = generate_student_number,
        verbose_name="Numero d'enregistrement"
    )
    
    name = models.CharField(max_length=200, verbose_name="Nom")
    firstname = models.CharField(max_length=200, verbose_name="Prenom")
    arabic_name = models.CharField(max_length=200, default="", verbose_name="Nom complet en Arabe")
    
    #other_name = models.CharField(max_length=200, blank=True, verbose_name="Dexieme Nom")
    gender        = models.CharField(max_length=10, choices=GENDER_CHOICES, default="male", verbose_name="Genre")
    nationality   = models.CharField(max_length=20, default="",verbose_name="Nationnalite")
    date_of_birth = models.DateField(default=timezone.now, verbose_name="Date de Naissance")
    birth_city    = models.CharField(max_length=10, choices=CITYES_CHOICE, default="Niamey", verbose_name="Niamey")
    
    current_class = models.ForeignKey(
        StudentClass, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Classe actuelle"
    )
    date_of_admission    = models.DateField(default=timezone.now, verbose_name="Date d'admission")

    parent_mobile_number = models.CharField(
        validators       = [mobile_num_regex], max_length=13, blank=True, verbose_name="Contact parent"
    )

    has_learned_quran = models.CharField(max_length=20, choices=HAS_LEARNED_QURAN, default="yes", verbose_name="J'aide deja appris le Coran ", blank=True,)
    health_state      = models.CharField(max_length=20, choices=HEALTH_STATE_CHOICES,default="healthy", verbose_name="Etat de Sante")
    health_type       = models.CharField(max_length=100, default="Aucun", verbose_name="Type de Maladie")
    passport          = models.ImageField(blank=True, upload_to="students/passports/", verbose_name="Carte d'identite")

    address = models.TextField(blank=True)
    
    others = models.TextField(blank=True, verbose_name="Plus de details")
    
    class Meta:
        ordering = ["name", "firstname" ]

    def get_absolute_url(self):
       return reverse("student-detail", kwargs={"pk": self.pk})
    
    def save(self, *args, **kwargs):
        if not self.registration_number:
            # Get the latest student register number
            last_student = Student.objects.order_by('-id').first()
            if last_student:
                last_register_number = last_student.registration_number
                # Extract the numeric part of the register number
                last_number = int(last_register_number.split('-')[1])
            else:
                # If no students exist yet, start with 0
                last_number = 0
            # Increment the numeric part
            new_number = last_number + 1
            # Format the new register number with the prefix and padded numeric part
            self.registration_number = 'M-{0:03d}'.format(new_number)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name} {self.firstname} ({self.registration_number})"
    
class StudentBulkUpload(models.Model):
    date_uploaded = models.DateTimeField(auto_now=True)
    csv_file = models.FileField(upload_to="students/bulkupload/")
