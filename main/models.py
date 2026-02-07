from django.db.models import (
Model, 
CharField, 
IntegerField,
ForeignKey, 
EmailField,
DateTimeField,
CASCADE,
UniqueConstraint,
BooleanField,
)
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField

from datetime import datetime, timedelta

def validate_social_tag(value):
    if value and not value.startswith('@'):
        raise ValidationError('Тег должен начинаться с символа @.')

class Doctor(Model):
    name = CharField(max_length=100)
    family = CharField(max_length=100)
    second_name = CharField(max_length=100)
    specialty = CharField(max_length=200)
    experience = IntegerField()
    phone = PhoneNumberField(null=True, blank=False, unique=True)
    is_deleted = BooleanField(default=False)

    def __str__(self):
        return f"{self.family} {self.name} {self.second_name}"

class Patient(Model):
    name = CharField(max_length=100)
    family = CharField(max_length=100)
    second_name = CharField(max_length=100)
    phone = PhoneNumberField(null=True, blank=False, unique=True)
    tag_social = CharField(
        max_length=100,
        validators=[validate_social_tag])
    email = EmailField(max_length=200, null=False, blank=False, unique=True)
    is_deleted = BooleanField(default=False)

    def __str__(self):
        return f"{self.family} {self.name} {self.second_name}"
    

class Clinic(Model):
    name = CharField(max_length=100)
    juridical_address = CharField(max_length=1000)
    physical_address = CharField(max_length=1000)
    is_deleted = BooleanField(default=False)

    def __str__(self):
        return self.name
    
class Consult(Model):    
    create_date = DateTimeField(auto_now_add=True)
    update_date = DateTimeField(auto_now=True)
    start_date = DateTimeField(null=False)
    end_date = DateTimeField(blank=True, null=True)
    is_deleted = BooleanField(default=False)

    doctor = ForeignKey(Doctor, on_delete=CASCADE)
    patient = ForeignKey(Patient, on_delete=CASCADE)
    clinic = ForeignKey(Clinic, on_delete=CASCADE)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['doctor', 'start_date'],
                name='unique_doctor_start_date'
            )
        ]

    def clean(self):
        super().clean()
        if self.start_date and not self.end_date:
            self.end_date = self.start_date + timedelta(minutes=4)
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValidationError({
                'end_date': 'Дата окончания не может быть раньше даты начала.'
            })
        if self.doctor and self.start_date and self.end_date:
            overlapping = Consult.objects.filter(
                doctor=self.doctor,
                start_date__lt=self.end_date,   # его начало < нашего конца
                end_date__gt=self.start_date    # его конец > нашего начала
            ).exclude(pk=self.pk)

            if overlapping.exists():
                raise ValidationError('У врача уже есть приём в это время.')
        
    def save(self, *args, **kwargs):
        self.validate_end_date()  
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.clinic}, {self.doctor}, {self.patient}, {self.start_date}, {self.end_date}"
