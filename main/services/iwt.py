from main.redis import RefreshTokenStorage
import jwt
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()


@dataclass
class JwtAuth:
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))

    token_storage = RefreshTokenStorage(
        TTL=timedelta(minutes=REFRESH_TOKEN_EXPIRE_DAYS)
    )

    def create_tokens(self, user_id: str):
        access_token = self._encode_jwt(
            payload={"sub": user_id},
            expires_delta=timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES),
        )
        refresh_token = self._encode_jwt(
            payload={"sub": user_id},
            expires_delta=timedelta(days=self.REFRESH_TOKEN_EXPIRE_DAYS),
        )

        # Сохраняем refresh_token в DB 1
        self.token_storage.save_token(token=refresh_token, user_id=user_id)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    def _encode_jwt(self, payload: dict, expires_delta: timedelta):
        expire = datetime.now(timezone.utc) + expires_delta
        payload.update({"exp": expire})
        return jwt.encode(payload, self.SECRET_KEY, algorithm=self.ALGORITHM)

    def decode_jwt(self, token: str):
        try:
            data = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
        except jwt.ExpiredSignatureError:
            raise Exception("Token expired")
        except jwt.InvalidTokenError:
            raise Exception("Invalid token")
        return data.get("sub")

    def verify_refresh_token(self, token: str) -> str:
        """Проверяет существование refresh-токен в Redis"""
        user_id = self.token_storage.get_token(token=token)
        if not user_id:
            raise ValueError("Invalid or expired refresh token")
        return user_id

    def revoke_refresh_token(self, token: str):
        """Удаляет refresh-токен"""
        self.token_storage.revoke_token(token=token)
