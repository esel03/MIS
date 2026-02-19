from dataclasses import dataclass
from main.repositories.base import RepositoryBase
from .auth_jwt import JwtAuth
from django.db.models import Model

repository = RepositoryBase()
jwt_auth = JwtAuth()


@dataclass
class AuthorizationService:
    model: Model

    def register_user(self, user_model, data):
        """Регистрация пользователя."""
        return repository.record_one(model=user_model, **data)

    def login_user(self, user_model, data):
        """Авторизация пользователя."""
        user = repository.is_exists(
            model=self.model, field="email", value=data["email"]
        )
        return jwt_auth.create_tokens(user_id=data["id"])
