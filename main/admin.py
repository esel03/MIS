from django.contrib import admin
from .models import Patient, Doctor, Clinic, Consult

"""
@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "family",
        "second_name",
        "age",
        "gender",
        "phone_number",
        "email",
    )
    ordering = ("family", "name", "second_name", )


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    pass


@admin.register(Clinic)
class ClinicAdmin(admin.ModelAdmin):
    pass


@admin.register(Consult)
class ConsultAdmin(admin.ModelAdmin):
    pass

"""