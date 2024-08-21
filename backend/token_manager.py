import jwt
from rest_framework import exceptions as exc
from .settings import SECRET_KEY
from datetime import datetime, timedelta

class TokenManager:
    ALGORITHM = 'HS256'
    ACCESS_LIFETIME = {
        'days': 0,
        'minutes': 5
    }
    REFRESH_LIFETIME = {
        'days': 7
    }
    EXPIRE_FIELD = 'exp'
    USER_FIELD = 'user_id'
    IAT_FIELD = 'iat'

    @classmethod
    def generate_payload(cls, user_id:int | str, lifetime:dict, **kwargs) -> dict:
        payload:dict =  {
            cls.USER_FIELD: user_id,
            cls.EXPIRE_FIELD: datetime.now() + timedelta(**lifetime),
            cls.IAT_FIELD: datetime.now()
        }
        if kwargs:
            payload.update(**kwargs)
        return payload

    @classmethod
    def generate_access_token(cls, user, **kwargs) -> str:
        access_token_payload = cls.generate_payload(user.id, cls.ACCESS_LIFETIME, **kwargs)
        access_token = jwt.encode(access_token_payload,
                                  SECRET_KEY, 
                                  algorithm=cls.ALGORITHM)
        return access_token

    @classmethod
    def generate_refresh_token(cls, user, **kwargs) -> str:
        refresh_token_payload = cls.generate_payload(user.id, cls.REFRESH_LIFETIME, **kwargs)
        refresh_token = jwt.encode(refresh_token_payload, 
                                   SECRET_KEY,
                                   algorithm=cls.ALGORITHM)
        return refresh_token
    
    @classmethod
    def decode_token(cls, encoded_token:str) -> dict:
        try:
            payload = jwt.decode(encoded_token, SECRET_KEY, algorithms=[cls.ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise exc.AuthenticationFailed('Access token expired.', 403)
        
    @classmethod
    def get_credentials(cls, encoded_token:str, credentials:list | None=None) -> list:
        decoded_token = cls.decode_token(encoded_token)
        user_id = decoded_token.get(cls.USER_FIELD)
        result = [user_id]
        if credentials:
            for key in credentials:
                result.append(decoded_token.get(key))
        return tuple(result)