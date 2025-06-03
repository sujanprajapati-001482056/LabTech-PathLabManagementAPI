from django.db import models
from django.utils.translation import gettext_lazy as _

class Patient(models.Model):
    """Model for patient information."""
    
    # Basic information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    
    # Gender choices
    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'
    
    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other'),
    ]
    
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    
    # Contact information
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    
    # Medical information
    blood_group = models.CharField(max_length=10, blank=True, null=True)
    allergies = models.TextField(blank=True, null=True)
    
    # Emergency contact
    emergency_contact_name = models.CharField(max_length=200, blank=True, null=True)
    emergency_contact_phone = models.CharField(max_length=15, blank=True, null=True)
    emergency_contact_relationship = models.CharField(max_length=50, blank=True, null=True)
    
    # Registration information
    registration_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        ordering = ['-registration_date']

class MedicalHistory(models.Model):
    """Model for patient medical history."""
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_histories')
    diagnosis = models.CharField(max_length=200)
    treatment = models.TextField()
    date = models.DateField()
    doctor = models.CharField(max_length=200)
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.patient} - {self.diagnosis} ({self.date})"
    
    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'Medical histories'