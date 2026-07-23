from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
class PasswordManager:
    def __init__(self):
        self.ph = PasswordHasher()
    def hash_password(self, password: str) -> str:
        return self.ph.hash(password)
    def verify_password(
        self,
        password: str,
        password_hash: str
    ) -> bool:
        try:
            return self.ph.verify(
                password_hash,
                password
            )
        except VerifyMismatchError:
            return False
        except Exception:
            return False
