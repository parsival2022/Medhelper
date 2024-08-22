from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication, get_authorization_header, _
from backend.error_manager import ErrorManager as em
from backend.token_manager import TokenManager as tm
from backend.settings import AUTH_HEADER
from .models import User

class Authentication(TokenAuthentication):

    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None
        parsed_token = tm.check_and_parse_raw_token(auth)
        return self.authenticate_credentials(parsed_token)
    
    def authenticate_credentials(self, token):
        user_id, current_role = tm.get_credentials(token, ['current_role'])
        try:
            user = User.objects.get(id=user_id)
            user.create_auth_instance(current_role=current_role)
            return (user, token)
        except User.DoesNotExist:
            raise em.AuthenticationFailed()

