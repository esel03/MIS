from rest_framework import serializers
from main.models import Patient
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError as DjangoValidationError
import json


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        exclude = ["is_deleted"]
        extra_kwargs = {'password': {'write_only': True}}
        
    def validate_password(self, value):
        if not value:
            raise serializers.ValidationError("Пароль обязателен.")
        return make_password(value) 

    def validate_email(self, value):
        if self.instance is None:
            if Patient.objects.filter(email=value).exists():
                raise serializers.ValidationError("Пациент с таким email уже существует.")
        else:
            if Patient.objects.filter(email=value).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError("Пациент с таким email уже существует.")
        return value

    def validate_phone(self, value):
        if value:
            if self.instance is None:
                if Patient.objects.filter(phone=value).exists():
                    raise serializers.ValidationError("Пациент с таким телефоном уже существует.")
            else:
                if Patient.objects.filter(phone=value).exclude(pk=self.instance.pk).exists():
                    raise serializers.ValidationError("Пациент с таким телефоном уже существует.")
        return value

    def validate_tag_social(self, value):
        if not value:
            raise serializers.ValidationError("Поле tag_social обязательно.")
        return value
    
    def create(self, validated_data):
        patient = Patient.objects.create(**validated_data)
        return patient