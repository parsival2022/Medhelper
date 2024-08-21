from .models import User, MedicalEmployeeProfile, PatientProfile, Organisation, Administrator
from rest_framework.serializers import ModelSerializer

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class MedicalEmployeeSerializer(ModelSerializer):
    class Meta:
        model = MedicalEmployeeProfile
        fields = '__all__'

class PatientSerializer(ModelSerializer):
    class Meta:
        model = PatientProfile
        fields = '__all__'

class AdministratorSerializer(ModelSerializer):
    class Meta:
        model = Administrator
        fields = '__all__'

class OrganisationSerializer(ModelSerializer):
    class Meta:
        model = Organisation
        fields = '__all__'