from main.models import Patient
from main.repositories.base import BaseRepository


class RepositoryPatient:
    def get_patient_by_id(self, patient_id: int) -> Patient:
        return Patient.objects.get(id=patient_id)
