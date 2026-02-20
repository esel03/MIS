from django.db import models
from typing import Type
from rest_framework import serializers
from dataclasses import dataclass
from django.contrib.auth.hashers import make_password
from ..repositories.base import RepositoryBase

repo = RepositoryBase()


class BaseSerializer(serializers.ModelSerializer):

    def validate_password(self, value):
        if not value:
            raise serializers.ValidationError("Пароль обязателен.")
        return make_password(value)


    def validate_email(self, value):
        if value:
            if not hasattr(self.Meta, 'model'):
                raise AssertionError("Сериализатор должен иметь Meta.model")
            model = self.Meta.model
            if repo.is_exists(model=model, field='email', value=value):
                raise serializers.ValidationError("Пользователь с таким email уже существует.")
            return value
        else:
            raise serializers.ValidationError("Поле не может быть пустым.")


    def validate_phone(self, value):
        if value:
            if not hasattr(self.Meta, 'model'):
                raise AssertionError("Сериализатор должен иметь Meta.model")
            model = self.Meta.model
            if repo.is_exists(model=model, field='phone', value=value):
                raise serializers.ValidationError("Пользователь с таким телефоном уже существует.")
            return value
        else:
            raise serializers.ValidationError("Поле не может быть пустым.")