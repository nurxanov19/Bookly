from passlib.context import CryptContext
from datetime import datetime, timedelta
import uuid, jwt
from src.config import Config

import logging


passwd_context = CryptContext(schemes=['bcrypt'])

ACCESS_TOKEN_EXPIRY = 3600

def generate_password_hash(password: str) -> str:
    hashed_pswrd = passwd_context.hash(password)
    return hashed_pswrd

def check_password_hash(password: str, hash: str) -> bool:
    return passwd_context.verify(password, hash)

def verify_password(password: str, hash: str) -> bool:
    return passwd_context.verify(password, hash)

def create_access_token(user_data: dict, expiry: timedelta = None, refresh: bool= False):

    payload = {}
    payload['user'] = user_data
    payload['exp'] = datetime.now() + (expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY))
    payload['jti'] = str(uuid.uuid4())
    payload['refresh'] = refresh

    token = jwt.encode(payload=payload, key=Config.JWT_SECRET_KEY, algorithm=Config.JWT_ALGORITHM)
    return token


def decode_token(token: str) -> str:
    try:
        token_data = jwt.decode(jwt=token, key=Config.JWT_SECRET_KEY, algorithms=[Config.JWT_ALGORITHM])
        return token_data

    except jwt.PyJWTError as e:
        logging.exception(e)
        return None
