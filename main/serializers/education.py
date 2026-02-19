from rest_framework import serializers
from datetime import datetime
from dataclasses import dataclass
from ..models import Education, University, Ordination, AdvTraining


class EducationSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Education.
    Принимает и валидирует JSON-поле history_education.
    """

    class Meta:
        model = Education
        fields = '__all__'

    def validate_history_education(self, value):
        """
        Валидация поля history_education (входящий JSON).
        Вызывается при создании/обновлении.
        """
        if not isinstance(value, dict):
            raise serializers.ValidationError("Поле 'history_education' должно быть объектом (словарём).")

        required_keys = ["universities", "ordinator", "advanced_training"]
        optional_keys = ["advanced_training"]

        for key in required_keys:
            self._validate_required_list(key, value)
        return value

        for key in optional_keys:
            self._validate_required_list(key, value)
        return value

    def _validate_required_list(self, key: str, data: dict):
        if key not in data:
            raise serializers.ValidationError({key: f"Обязательное поле '{key}' отсутствует."})
        self._validate_list_content(data[key], key)


    def _validate_list_content(self, items, parent_key: str):
        if not isinstance(items, list):
            raise serializers.ValidationError({parent_key: f"Поле '{parent_key}' должно быть списком."})

        for item in items:
            if not isinstance(item, dict):
                raise serializers.ValidationError({f"{parent_key}[{item}]": "Элемент должен быть словарем."})

            errors = {}
            name = item.get("name")
            if not name or not isinstance(name, str) or not name.strip():
                errors["name"] = "Обязательное непустое строковое поле."

            specialty = item.get("specialty")
            if not specialty or not isinstance(specialty, str) or not specialty.strip():
                errors["specialty"] = "Обязательное непустое строковое поле."

            start_date = item.get("start_date")
            if not start_date or not isinstance(start_date, str) or not start_date.strip():
                start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
                errors["start_date"] = "Обязательная строка в формате даты."

            end_date = item.get("end_date")
            if not end_date or not isinstance(end_date, str) or not start_date.strip():
                end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
                errors["end_date"] = "Обязательная строка в формате даты."

            if start_date >= end_date:
                errors["date"] = "Начало обучения не может быть позже конца обучения."


            if errors:
                raise serializers.ValidationError({f"{parent_key}[{item}]": errors})