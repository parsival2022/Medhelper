from rest_framework.permissions import BasePermission
from .models import User

class IsNotAuthenticated(BasePermission):
    message = "You are already logged in."
    def has_permission(self, request, view):
        return not request.user.is_authenticated
    
class IsNotRegistered(BasePermission):
    message = "You are already registered."
    def has_permission(self, request, view):
        email = request.data['email']
        try:
            user = User.objects.get(email=email)
            if user: return False
        except User.DoesNotExist:
            return True
