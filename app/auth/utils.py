from datetime import datetime

import jwt
import bcrypt
from asyncpg.pgproto.pgproto import timedelta

from core.config import settings


def encode_jwt(
        payload: dict,
        private_key = settings.auth.private_key_path.read_text(),
        algorithm: str = settings.auth.algorithm,
):
    to_encode = payload.copy()
    to_encode.update(
        exp=datetime.utcnow() + timedelta(minutes=3)
    )
    encoded_jwt = jwt.encode(payload=to_encode, key=private_key, algorithm=algorithm)
    return encoded_jwt


def decode_jwt(
        token,
        public_key: str = settings.auth.public_key_path.read_text(),
        algorithm: str = settings.auth.algorithm,
):
    decoded_jwt = jwt.decode(token, public_key, algorithms=[algorithm])
    return decoded_jwt


def hashcode_pw(
        password: str,
):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def validate_passwords(
        password: str,
        hash_pw,
):
    return bcrypt.checkpw(password.encode(), hash_pw)