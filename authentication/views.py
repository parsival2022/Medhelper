from rest_framework.views import APIView
from rest_framework.serializers import ValidationError
from rest_framework.status import *
from rest_framework.response import Response
from backend.error_manager import ErrorManager as em
from backend.token_manager import TokenManager as tm
from .permissions import IsNotAuthenticated, IsNotRegistered
from .serializers import *
from .decorators import handle_errors_with_response


class Registration(APIView):
    permission_classes = (IsNotAuthenticated, IsNotRegistered)

    @handle_errors_with_response
    def post(request):
        data = request.data
        serializer = UserSerializer(data)

        serializer.is_valid()
        new_user = serializer.save()
        tokens = tm.generate_refresh_access_pair(new_user, current_role=None)
        return Response(tokens, HTTP_201_CREATED)


