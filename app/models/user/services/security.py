import hashlib
import secrets


def generate_token():
    return secrets.token_urlsafe()

def get_password_hash(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()
