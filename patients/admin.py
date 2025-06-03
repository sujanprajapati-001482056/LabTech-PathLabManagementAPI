from django.contrib import admin
from .models import Patient, MedicalHistory

class MedicalHistoryInline(admin.TabularInline):
    model = MedicalHistory
    extra = 0

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'gender', 'phone_number', 'registration_date')
    list_filter = ('gender', 'registration_date')
    search_fields = ('first_name', 'last_name', 'phone_number', 'email')
    date_hierarchy = 'registration_date'
    inlines = [MedicalHistoryInline]

@admin.register(MedicalHistory)
class MedicalHistoryAdmin(admin.ModelAdmin):
    list_display = ('patient', 'diagnosis', 'date', 'doctor')
    list_filter = ('date',)
    search_fields = ('patient__first_name', 'patient__last_name', 'diagnosis', 'doctor')