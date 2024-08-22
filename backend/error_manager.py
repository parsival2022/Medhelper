from rest_framework.response import Response
from rest_framework.status import *

class ErrorResponse:
    msg = 'Ooops! Something went wrong...'
    _status = HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(self, msg=None, status=None) -> None:
        if msg:
            self.msg = msg   
        if status:
            self._status = status     

    def response(self, **kwargs):
        return Response({'error_message': self.msg}, self._status, **kwargs)
    
class ErrorWithResponse(Exception):
    detail = 'Ooops! Something went wrong...'
    code = HTTP_500_INTERNAL_SERVER_ERROR
    response_obj = ErrorResponse(detail, code)
    
    def response(self, **kwargs): 
        return self.response_obj.response(**kwargs)
    
class ErrorManager:
    class SerializerErrorResponse(ErrorWithResponse):
        code = HTTP_400_BAD_REQUEST

        def __init__(self, errors=None):
            if errors:
                self.detail = self.format_msg(errors)

        def format_msg(self, errors):
            e_msg = {}
            for field_name, field_errors in errors.items():
                e_msg[field_name] = ', '.join([detail.string for detail in field_errors])

            return e_msg
        
    class NoRequiredCredentialsErrorResponse(ErrorWithResponse):
        detail = "No required credentials, such as email or password, was provided"
        code = HTTP_400_BAD_REQUEST

    class ValidationErrorResponse(ErrorWithResponse):
        detail = 'Provided data failed validation check.'
        code = HTTP_400_BAD_REQUEST

    class UnknownErrorResponse(ErrorWithResponse):
        pass
        
    class AuthenticationFailed(ErrorWithResponse):
        detail = 'User with provided credentials does not exist.'
        code = HTTP_401_UNAUTHORIZED