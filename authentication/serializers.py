import re
from rest_framework.serializers import ModelSerializer, ValidationError
from .models import User, MedicalEmployeeProfile, PatientProfile, Organisation, Administrator
from backend.error_manager import ErrorManager as em

class CustomModelSerializer(ModelSerializer):
    def is_valid(self, *, raise_exception=True):
        try:
            return super().is_valid(raise_exception=raise_exception)
        except ValidationError as e:
            raise em.SerializerErrorResponse(self.errors)

class UserSerializer(CustomModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def validate_password(self, password):
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        
        def regex_check(password, regex, msg):
            if not re.search(regex, password):
                raise ValidationError(msg)
            
        options = [
            (r'[A-Z]', "Password must contain at least one uppercase letter."),
            (r'[a-z]', "Password must contain at least one lowercase letter."),
            (r'[0-9]', "Password must contain at least one digit."),
            (r'[!@#$%^&*(),.?":{}|<>]', "Password must contain at least one special character.")
        ]
        
        for regex, msg in options:
            regex_check(password, regex, msg)
        
        return password


class MedicalEmployeeSerializer(CustomModelSerializer):
    class Meta:
        model = MedicalEmployeeProfile
        fields = '__all__'

class PatientSerializer(CustomModelSerializer):
    class Meta:
        model = PatientProfile
        fields = '__all__'

class AdministratorSerializer(CustomModelSerializer):
    class Meta:
        model = Administrator
        fields = '__all__'

class OrganisationSerializer(CustomModelSerializer):
    class Meta:
        model = Organisation
        fields = '__all__'