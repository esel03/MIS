from dataclasses import dataclass
from main.models import Patient
from main.repositories.base import RepositoryBase

@dataclass
class PatientRepository(RepositoryBase):
    model = Patient
