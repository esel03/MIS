from rest_framework.response import Response
from rest_framework import status
from ..repositories.doctor import DoctorRepository
from ..serializers.doctor import DoctorCreateUpdateSerializer
from ..models import Doctor
from dataclasses import dataclass


@dataclass
class DoctorService:
    repository = DoctorRepository()

    def create_doctor(self, data: dict):
        serializer = DoctorCreateUpdateSerializer(data=data)
        if serializer.is_valid():
            result = serializer.validated_data
            if (temp := self.repository.record_one(model=Doctor, **result)):
                print('RESULT===\n', temp)
                return {"status": status.HTTP_201_CREATED}
            print('RESULT===\n', temp)
            return {"status": status.HTTP_400_BAD_REQUEST}
        else:
            return {"errors": serializer.errors, "status": "error"}
