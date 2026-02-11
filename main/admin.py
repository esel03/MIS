from django.contrib import admin
from .models import Patient, Doctor, Clinic, Consult, Education


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = [
        "doctor",
        "history_education",
    ]


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = [
        "family",
        "name",
        "second_name",
        "gender",
        "phone",
        "email",
    ]
    ordering = ("family", "name", "second_name", )


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = [
        "family",
        "name",
        "second_name",
        "gender",
        "phone",
        "email",
    ]
    ordering = ("family", "name", "second_name", )


@admin.register(Clinic)
class ClinicAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "juridical_address",
    ]
    ordering = ("name", "juridical_address", )
        

@admin.register(Consult)
class ConsultAdmin(admin.ModelAdmin):
    pass

