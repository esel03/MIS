from dataclasses import dataclass
from rest_framework import serializers
from ..models import Doctor
from ..serializers.base import BaseSerializer


class DoctorCreateUpdateSerializer(BaseSerializer):
    class Meta:
        model = Doctor
        exclude = ['is_deleted']
        extra_kwargs = {
            'password': {'write_only': True}
        }

