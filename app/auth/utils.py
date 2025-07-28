import jwt
import bcrypt

from core.config import settings


def encode_jwt(
        payload: dict,
        private_key: str = settings.auth.private_key_path,
        algorithm: str = settings.auth.algorithm,
):
    encoded_jwt = jwt.encode(payload, private_key, algorithm=algorithm)
    return encoded_jwt


def decode_jwt(
        token,
        public_key: str = settings.auth.public_key_path,
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