from dataclasses import dataclass
from main.repositories.base import RepositoryBase


@dataclass
class RegistrationUser:
    repository = RepositoryBase()

    def register_user(self, user_model, data):
        """Регистрация пользователя."""
        return self.repository.record_one(user_model, **data)
