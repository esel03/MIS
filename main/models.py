from django.db import models
from django.db.models import CASCADE
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField
from main.validation_model import (
validate_required_fields,
validate_optional_field,
validate_social_tag,
)

import json
from django.core.serializers.json import DjangoJSONEncoder
from datetime import timedelta




class BaseModel(models.Model):
    """
    gender: Женщина - False, Мужчина - True
    """

    name = models.CharField(max_length=100, null=False, verbose_name="Имя пользователя")
    family = models.CharField(
        max_length=100, null=False, verbose_name="Фамилия пользователя"
    )
    second_name = models.CharField(
        max_length=100, null=False, verbose_name="Отчество пользователя"
    )
    gender = models.BooleanField(
        default=False, null=False, verbose_name="Пол пользователя"
    )
    email = models.EmailField(
        max_length=200,
        null=False,
        blank=False,
        unique=True,
        verbose_name="Почта пользователя",
    )
    phone = PhoneNumberField(
        null=True, blank=False, unique=True, verbose_name="Номер телефона пользователя"
    )
    password = models.CharField(max_length=100, null=False, verbose_name="Пароль")
    is_deleted = models.BooleanField(
        default=False, verbose_name="Флаг удаленности аккаунта пользователя"
    )

    class Meta:
        abstract = True


class Doctor(BaseModel):
    date_birth = models.DateField(null=False, verbose_name="Дата рождения")
    date_start_work = models.DateField(null=False, verbose_name="Дата начала работы")
    date_end_work = models.DateField(
        null=True, blank=True, verbose_name="Дата конца работы"
    )
    salary = models.IntegerField(null=False, verbose_name="Зарплата врача")
    specialty = models.CharField(max_length=200, verbose_name="Специализация врача")
    experience = models.IntegerField(verbose_name="Опыт врача")

    def clean(self):
        super().clean()
        if not self.date_birth:
            raise ValidationError("Дата рождения должна быть указана.")
        if not self.date_start_work:
            raise ValidationError("Дата начала работы должна быть указана.")
        if self.date_birth > self.date_start_work:
            raise ValidationError(
                "Дата начала работы не может быть раньше даты рождения."
            )
        if self.date_end_work and self.date_start_work > self.date_end_work:
            raise ValidationError(
                "Дата начала работы не может быть позже даты окончания работы."
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        if self.second_name:
            return f"{self.family} {self.name} {self.second_name}"
        return f"{self.family} {self.name}"


class Education(models.Model):
    doctor = models.ForeignKey(
        Doctor, on_delete=CASCADE, verbose_name="ForeignKey на врача"
    )
    history_education = models.JSONField(
        encoder=DjangoJSONEncoder, verbose_name="История обучения врача"
    )

    def clean(self):
        super().clean()
        data = self.history_education

        # Проверка типа
        if not isinstance(data, dict):
            raise ValidationError(
                "Поле 'history_education' должно быть объектом (словарём)."
            )

        required_fields = ["universities", "ordinator"]
        optional_fields = ["advanced_training"]
        for key in required_fields:
            validate_required_fields(key=key, data=data)
        for key in optional_fields:
            validate_optional_field(key=key, data=data)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Образование: {self.doctor}"


class Patient(BaseModel):
    tag_social = models.CharField(
        max_length=100,
        validators=[validate_social_tag],
        verbose_name="Имя аккаунта в социальных сетях",
    )

    def __str__(self):
        return f"{self.family} {self.name} {self.second_name}"


class Clinic(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название клиники")
    juridical_address = models.CharField(
        max_length=1000, verbose_name="Юридический адрес клиники"
    )
    physical_address = models.CharField(
        max_length=1000, verbose_name="Физический адрес клиники"
    )
    doctors = models.ManyToManyField(Doctor, verbose_name="m2m связь с таблицей врачей")
    is_deleted = models.BooleanField(
        default=False, verbose_name="Флаг удаленности клиники"
    )

    def __str__(self):
        return f"{self.name}"


class Admin(BaseModel):
    clinic = models.ForeignKey(
        Clinic, on_delete=CASCADE, verbose_name="ForeignKey на клинику"
    )

    def __str__(self):
        return f"{self.family} {self.name} {self.second_name}"


class Consult(models.Model):
    create_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания консультации"
    )
    update_date = models.DateTimeField(
        auto_now=True, verbose_name="Дата обновления консультации"
    )
    start_date = models.DateTimeField(
        null=False, verbose_name="Дата начала консультации"
    )
    end_date = models.DateTimeField(
        blank=True, null=True, verbose_name="Дата конца консультации"
    )
    is_deleted = models.BooleanField(
        default=False, verbose_name="флаг удалённости консультации"
    )

    doctor = models.ForeignKey(
        Doctor, on_delete=CASCADE, verbose_name="ForeignKey на врача"
    )
    patient = models.ForeignKey(
        Patient, on_delete=CASCADE, verbose_name="ForeignKey на пациента"
    )
    clinic = models.ForeignKey(
        Clinic, on_delete=CASCADE, verbose_name="ForeignKey на клинику"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["doctor", "start_date"], name="unique_doctor_start_date"
            )
        ]

    def clean(self):
        super().clean()
        if self.start_date and not self.end_date:
            self.end_date = self.start_date + timedelta(minutes=4)
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValidationError(
                {"end_date": "Дата окончания не может быть раньше даты начала."}
            )
        if self.doctor and self.start_date and self.end_date:
            overlapping = Consult.objects.filter(
                doctor=self.doctor,
                start_date__lt=self.end_date,
                end_date__gt=self.start_date,
            ).exclude(pk=self.pk)

            if overlapping.exists():
                raise ValidationError("У врача уже есть приём в это время.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.clinic}, {self.doctor}, {self.patient}, {self.start_date}, {self.end_date}"
