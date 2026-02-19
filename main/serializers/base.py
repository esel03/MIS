from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from ..repositories.base import RepositoryBase

repo = RepositoryBase()


class BaseSerializer(serializers.ModelSerializer):
    @staticmethod
    def validate_password(value):
        if not value:
            raise serializers.ValidationError("Пароль обязателен.")
        return make_password(value)

    @staticmethod
    def validate_email(model, field, value):
        if value:
            if not repo.is_exists(model=model, field=field, value=value):
                raise serializers.ValidationError("Пользователь с таким email уже существует.")
            return value
        else:
            raise serializers.ValidationError("Поле не может быть пустым.")

    @staticmethod
    def validate_phone(model,field, value):
        if value:
            if not repo.is_exists(model=model, field=field, value=value):
                raise serializers.ValidationError("Пациент с таким телефоном уже существует.")
            return value
        else:
            raise serializers.ValidationError("Поле не может быть пустым.")