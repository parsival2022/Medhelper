from functools import wraps
from backend.error_manager import ErrorWithResponse, ErrorManager as em

def handle_errors_with_response(func):
    @wraps(func)
    def _wrapped(request, *args, **kwargs):
        try:
            return func(request, *args, **kwargs)
        except ErrorWithResponse as e:
            return e.response()
        except Exception as e:
            return em.UnknownErrorResponse().response()
    return _wrapped