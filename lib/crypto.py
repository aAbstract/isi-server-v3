import os
import jwt
import hmac
import hashlib
from datetime import datetime, timedelta


_jwt_key: str = os.getenv('JWT_KEY')
_hmac_key: str = os.getenv('HMAC_KEY')


def create_jwt_token(data: dict) -> str:
    expiration_time = datetime.now() + timedelta(hours=24)
    data['exp'] = expiration_time
    return jwt.encode(data, _jwt_key, algorithm='HS512')


def decode_jwt_token(token: str) -> dict[str, dict]:
    return jwt.decode(token, _jwt_key, algorithms=['HS512'])


def hash_password(password: str) -> str:
    return hmac.new(_hmac_key.encode(), password.encode(), hashlib.sha512).hexdigest()
