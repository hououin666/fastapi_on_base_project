import jwt
import bcrypt


def encode_jwt(
        payload,
        private_key,
        algorith,
):
    encoded_jwt = jwt.encode(payload, private_key, algorithm="HS256")
    return encoded_jwt


def decode_jwt(
        token,
        public_key,
        algorithm,
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