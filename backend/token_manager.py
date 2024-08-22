import jwt
from datetime import datetime, timedelta
from rest_framework.authentication import _
from .settings import SECRET_KEY
from .error_manager import ErrorManager as em


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
    def generate_token(cls, user, lifetime, **kwargs):
        token_payload = cls.generate_payload(user.id, lifetime, **kwargs)
        token = jwt.encode(token_payload,
                           SECRET_KEY, 
                           algorithm=cls.ALGORITHM)
        return token

    @classmethod
    def generate_access_token(cls, user, **kwargs) -> str:
        return cls.generate_token(user, cls.ACCESS_LIFETIME, **kwargs)

    @classmethod
    def generate_refresh_token(cls, user, **kwargs) -> str:
        return cls.generate_token(user, cls.REFRESH_LIFETIME, **kwargs)
    
    @classmethod
    def decode_token(cls, encoded_token:str) -> dict:
        try:
            payload = jwt.decode(encoded_token, SECRET_KEY, algorithms=[cls.ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise em.AuthenticationFailed('Access token expired.', 403)
        
    @classmethod
    def generate_refresh_access_pair(cls, user, **kwargs) -> dict:
        return {
            'access_token': cls.generate_access_token(user, **kwargs),
            'refresh_token': cls.generate_refresh_token(user, **kwargs)
            }
        
    @classmethod
    def get_credentials(cls, encoded_token:str, credentials:list | None=None) -> list:
        decoded_token = cls.decode_token(encoded_token)
        user_id = decoded_token.get(cls.USER_FIELD)
        result = [user_id]
        if credentials:
            for key in credentials:
                result.append(decoded_token.get(key))
        return tuple(result)
    
    @classmethod
    def check_raw_token(cls, raw_token:list[str]) -> None:
        msg = None      
        if len(raw_token) == 1:
            msg = _('Invalid token header. No credentials provided or header is missed.')
        if len(raw_token) > 2:
            msg = _('Invalid token header. Token string should not contain spaces.')
        if msg: raise em.AuthenticationFailed(msg)

    @classmethod 
    def parse_raw_token(cls, raw_token:list[str]) -> str:
        try:
            token = raw_token[1].decode()
            return token
        except UnicodeError:
            msg = _('Invalid token header. Token string should not contain invalid characters.')
            raise em.AuthenticationFailed(msg)
        
    @classmethod
    def check_and_parse_raw_token(cls, raw_token:list[str]) -> str:
        cls.check_raw_token(raw_token)
        parsed_token = cls.parse_raw_token(raw_token)
        return parsed_token