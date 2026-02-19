from dataclasses import dataclass
from ..models import Doctor
from ..serializers.base import BaseSerializer

@dataclass
class DoctorSerializer(BaseSerializer):
    model = Doctor
    class Meta:
        model = Doctor
        extra_kwargs = {'password': {'write_only': True}}


