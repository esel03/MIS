from django.db import models
from django.db.models import CASCADE
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField

import json
from django.core.serializers.json import DjangoJSONEncoder
from datetime import timedelta

def validate_social_tag(value):
    if value and not value.startswith('@'):
        raise ValidationError('Тег должен начинаться с символа @.')
    
def default_education_history():
    """
{
  "universities": [
    {
      "name": "Медицинский университет",
      "specialty": "Лечебное дело",
      "start_date": "2010-09-01",
      "end_date": "2016-06-30"
    }
  ],
  "ordinator": [
    {
      "name": "Городская больница №1",
      "specialty": "Хирургия",
      "start_date": "2016-09-01",
      "end_date": "2017-08-31"
    }
  ],
  "advanced_training": [
    {
      "name": "Академия последипломного образования",
      "specialty": "Онкология",
      "start_date": "2020-03-01",
      "end_date": "2020-05-15"
    }
  ]
}
    """
    return {
        "universities": [],
        "ordinator": [],
        "advanced_training":[],
    }


class BaseModel(models.Model):
    """
    gender: Женщина - False, Мужчина - True
    """
    name = models.CharField(max_length=100, null=False)
    family = models.CharField(max_length=100, null=False)
    second_name = models.CharField(max_length=100, null=False)
    gender = models.BooleanField(default=False, null=False) 
    email = models.EmailField(max_length=200, null=False, blank=False, unique=True)
    phone = PhoneNumberField(null=True, blank=False, unique=True)
    password = models.CharField(max_length=100, null=False)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Doctor(BaseModel):
    date_birth = models.DateField(null=False)
    date_start_work = models.DateField(null=False)
    date_end_work = models.DateField(null=True, blank=True)
    salary = models.IntegerField(null=False)
    specialty = models.CharField(max_length=200)
    experience = models.IntegerField()

    def clean(self):
        super().clean()
        if not self.date_birth:
            raise ValidationError("Дата рождения должна быть указана.")
        if not self.date_start_work:
            raise ValidationError("Дата начала работы должна быть указана.")
        if self.date_birth > self.date_start_work:
            raise ValidationError("Дата начала работы не может быть раньше даты рождения.")
        if self.date_end_work and self.date_start_work > self.date_end_work:
            raise ValidationError("Дата начала работы не может быть позже даты окончания работы.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        if self.second_name:
            return f"{self.family} {self.name} {self.second_name}"
        return f"{self.family} {self.name}"

class Education(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=CASCADE)
    history_education = models.JSONField(
        encoder=DjangoJSONEncoder
    )

    def clean(self):
        super().clean()
        data = self.history_education

        # Проверка типа
        if not isinstance(data, dict):
            raise ValidationError("Поле 'history_education' должно быть объектом (словарём).")

        required_keys = ["universities", "ordinator", "advanced_training"]
        for key in required_keys:
            if key not in data:
                raise ValidationError(f"Отсутствует обязательное поле: '{key}'.")

            value = data[key]
            if not isinstance(value, list):
                raise ValidationError(f"Поле '{key}' должно быть списком.")

            for i, item in enumerate(value):
                if not isinstance(item, dict):
                    raise ValidationError(f"Элемент в списке '{key}[{i}]' должен быть объектом.")
                
                if "name" not in item or not isinstance(item["name"], str) or not item["name"].strip():
                    raise ValidationError(f"Запись в '{key}[{i}]' должна содержать непустое поле 'name'.")
                
                if "specialty" not in item or not isinstance(item["specialty"], str):
                    raise ValidationError(f"Запись в '{key}[{i}]' должна содержать поле 'specialty' (строка).")

                if "start_date" not in item or not isinstance(item["start_date"], str):
                    raise ValidationError(f"Запись в '{key}[{i}]' должна содержать поле 'start_date' (строка в формате даты).")

                if "end_date" not in item or not isinstance(item["end_date"], str):
                    raise ValidationError(f"Запись в '{key}[{i}]' должна содержать поле 'end_date' (строка в формате даты).")

    def save(self, *args, **kwargs):
        self.full_clean()  # Вызовет clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Образование: {self.doctor}"

class Patient(BaseModel):
    tag_social = models.CharField(
        max_length=100,
        validators=[validate_social_tag])

    def __str__(self):
        return f"{self.family} {self.name} {self.second_name}"
    

class Clinic(models.Model):
    name = models.CharField(max_length=100)
    juridical_address = models.CharField(max_length=1000)
    physical_address = models.CharField(max_length=1000)
    doctors = models.ManyToManyField(Doctor)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"
    

class Admin(BaseModel):
    clinic = models.ForeignKey(Clinic, on_delete=CASCADE)
    
class Consult(models.Model):    
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    start_date = models.DateTimeField(null=False)
    end_date = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    doctor = models.ForeignKey(Doctor, on_delete=CASCADE)
    patient = models.ForeignKey(Patient, on_delete=CASCADE)
    clinic = models.ForeignKey(Clinic, on_delete=CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
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
