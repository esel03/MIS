from dataclasses import dataclass
from ..models import Patient
from ..serializers.base import BaseSerializer

@dataclass
class PatientSerializer(BaseSerializer):
    model = Patient
    class Meta:
        model = Patient
        exclude = ["is_deleted"]
        extra_kwargs = {'password': {'write_only': True}}
