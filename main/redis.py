from django.core.cache import caches
from dataclasses import dataclass

cache_db = caches['default']
token_db = caches['tokens']

@dataclass
class RefreshTokenStorage:
    TTL: int  # 7 дней

    def save_token(self, token: str, user_id: str):
        token_db.set(token, user_id, timeout=self.TTL)

    @staticmethod
    def get_token(token: str) -> str | None:
        return token_db.get(token)

    @staticmethod
    def revoke_token(token: str):
        token_db.delete(token)
