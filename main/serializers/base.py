from rest_framework import serializers
from main.models import Doctor, Education
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError as DjangoValidationError
import json

class EducationInputSerializer(serializers.Serializer):
    """
    Валидация JSON-поля history_education
    """
    universities = serializers.ListField(
        child=serializers.DictField(), required=False, default=list
    )
    ordinator = serializers.ListField(
        child=serializers.DictField(), required=False, default=list
    )
    advanced_training = serializers.ListField(
        child=serializers.DictField(), required=False, default=list
    )

    def validate_universities(self, value):
        return self.validate_items(value, 'universities')

    def validate_ordinator(self, value):
        return self.validate_items(value, 'ordinator')

    def validate_advanced_training(self, value):
        return self.validate_items(value, 'advanced_training')

    def validate_items(self, items, parent_key):
        for i, item in enumerate(items):
            self.validate_item(item, parent_key, i)
        return items

    def validate_item(self, item, parent_key, index):
        errors = {}

        name = item.get("name")
        if not name or not isinstance(name, str) or not name.strip():
            errors["name"] = "Обязательное непустое строковое поле."

        specialty = item.get("specialty")
        if not specialty or not isinstance(specialty, str):
            errors["specialty"] = "Обязательное строковое поле."

        start_date = item.get("start_date")
        if not start_date or not isinstance(start_date, str):
            errors["start_date"] = "Обязательная строка в формате даты."

        end_date = item.get("end_date")
        if not end_date or not isinstance(end_date, str):
            errors["end_date"] = "Обязательная строка в формате даты."

        if errors:
            raise serializers.ValidationError({f"{parent_key}[{index}]": errors})

        return item


class DoctorCreateUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    education = EducationInputSerializer(required=False, allow_null=True)

    class Meta:
        model = Doctor
        exclude = ['is_deleted']

    def validate_email(self, value):
        if Doctor.objects.filter(email=value).exists():
            raise serializers.ValidationError("Врач с таким email уже существует.")
        return value

    def validate_phone(self, value):
        if Doctor.objects.filter(phone=value).exists():
            raise serializers.ValidationError("Врач с таким телефоном уже существует.")
        return value

    def validate(self, data):
        date_birth = data.get('date_birth')
        date_start_work = data.get('date_start_work')
        date_end_work = data.get('date_end_work')

        if date_birth and date_start_work and date_birth > date_start_work:
            raise serializers.ValidationError({
                'date_birth': 'Дата рождения не может быть позже даты начала работы.'
            })

        if date_end_work and date_start_work and date_start_work > date_end_work:
            raise serializers.ValidationError({
                'date_end_work': 'Дата окончания работы не может быть раньше даты начала.'
            })

        return data

    def create(self, validated_data):
        education_data = validated_data.pop('education', None)

        # Хешируем пароль
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])

        doctor = Doctor.objects.create(**validated_data)

        # Создаём образование
        if education_data:
            Education.objects.create(doctor=doctor, history_education=education_data)

        return doctor

    def update(self, instance, validated_data):
        education_data = validated_data.pop('education', None)

        # Обновляем пароль?
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Обновляем образование
        if education_data is not None:  # Явное обновление (null = удалить)
            if hasattr(instance, 'education'):
                instance.education.history_education = education_data
                instance.education.save()
            else:
                Education.objects.create(doctor=instance, history_education=education_data)

        elif education_data is None and hasattr(instance, 'education'):
            instance.education.delete()

        return instance