from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions as exc
from backend.settings import AUTH_HEADER
from backend.token_manager import TokenManager as tm
from .models import User

class Authentication(TokenAuthentication):
    def authenticate(self, request):
        return super().authenticate(request)
    
    def authenticate_credentials(self, token):
        user_id, current_role = tm.get_credentials(token, ['current_role'])
        try:
            user = User.objects.get(id=user_id)
            user.create_auth_instance(current_role=current_role)
            return (user, token)
        except User.DoesNotExist:
            raise exc.AuthenticationFailed('User with provided credentials does not exist.', 403)

