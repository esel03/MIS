# main/serializers/doctor.py
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from ..models import Doctor, Education


class EducationInputSerializer(serializers.Serializer):
    """
    Валидация поля history_education (вложенный JSON)
    """

    universities = serializers.ListField(child=serializers.DictField(), required=True)
    ordinator = serializers.ListField(child=serializers.DictField(), required=True)
    advanced_training = serializers.ListField(
        child=serializers.DictField(), required=False, allow_null=True, default=list
    )

    def validate_universities(self, value):
        return self._validate_list(value, "universities")

    def validate_ordinator(self, value):
        return self._validate_list(value, "ordinator")

    def _validate_list(self, items, field_name):
        if not isinstance(items, list):
            raise serializers.ValidationError(
                f"Поле '{field_name}' должно быть списком."
            )
        for i, item in enumerate(items):
            self._validate_item(item, field_name, i)
        return items

    def _validate_item(self, item, parent, index):
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
            raise serializers.ValidationError({f"{parent}[{index}]": errors})
        return item


class DoctorCreateUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    education = EducationInputSerializer(required=False, allow_null=True)

    class Meta:
        model = Doctor
        exclude = ["is_deleted"]

    def validate_email(self, value):
        if (
            Doctor.objects.filter(email=value)
            .exclude(pk=self.instance.pk if self.instance else None)
            .exists()
        ):
            raise serializers.ValidationError("Врач с таким email уже существует.")
        return value

    def validate_phone(self, value):
        if (
            Doctor.objects.filter(phone=value)
            .exclude(pk=self.instance.pk if self.instance else None)
            .exists()
        ):
            raise serializers.ValidationError("Врач с таким телефоном уже существует.")
        return value

    def validate(self, attrs):
        date_birth = attrs.get("date_birth")
        date_start_work = attrs.get("date_start_work")
        date_end_work = attrs.get("date_end_work")

        if date_birth and date_start_work and date_birth > date_start_work:
            raise serializers.ValidationError(
                {"date_birth": "Дата рождения не может быть позже даты начала работы."}
            )

        if date_end_work and date_start_work and date_start_work > date_end_work:
            raise serializers.ValidationError(
                {
                    "date_end_work": "Дата окончания работы не может быть раньше даты начала."
                }
            )

        return data

    def create(self, validated_data):
        education_data = validated_data.pop("education", None)
        validated_data["password"] = make_password(validated_data["password"])
        doctor = Doctor.objects.create(**validated_data)

        if education_data:
            Education.objects.create(doctor=doctor, history_education=education_data)

        return doctor

    def update(self, instance, validated_data):
        education_data = validated_data.pop("education", None)
        if "password" in validated_data:
            validated_data["password"] = make_password(validated_data["password"])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Обработка образования
        if education_data is not None:  # Явное обновление (null = удалить)
            if hasattr(instance, "education"):
                instance.education.history_education = education_data
                instance.education.save()
            else:
                Education.objects.create(
                    doctor=instance, history_education=education_data
                )
        elif education_data is None and hasattr(instance, "education"):
            instance.education.delete()

        return instance
