from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, email:str, password:str | None=None, **extra_fields:dict) -> AbstractBaseUser:
        if not email or not password:
            raise ValueError(f"The {'email' if not email else 'password'} field must be set")
        email = self.normalize_email(email)
        user:AbstractBaseUser = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=70)
    patronym = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, unique=True)
    date_of_registration = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'last_name', 'email', 'password')

    objects = UserManager()

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'

class PatientProfile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    height = models.DecimalField(max_digits=5, decimal_places=2)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    gender = models.CharField(max_length=1, choices=User.GENDER_CHOICES)
    birth_date = models.DateField()
    allergies = models.TextField(blank=True, null=True)
    surgeries = models.TextField(blank=True, null=True)
    injuries = models.TextField(blank=True, null=True)
    chronic_conditions = models.TextField(blank=True, null=True)
    vaccinations = models.TextField(blank=True, null=True)

    def calculate_age(self) -> int | None:
        if not self.birth_date:
            return None
        today = timezone.now().date()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))

    @property
    def age(self):
        return self.calculate_age()

class MedicalEmployeeProfile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialties = models.CharField(max_length=900)
    diploma_number = models.CharField(max_length=100)
    diploma_institution = models.CharField(max_length=255)
    study_start_date = models.DateField()
    study_end_date = models.DateField()
    courses = models.JSONField(default=dict)
    work_experience = models.JSONField(default=list)
    contacts = models.JSONField(default=dict)
    is_verified = models.BooleanField(default=False)

    REQUIRED_FIELDS = ('diploma_number', 'diploma_institution')


class Organisation(models.Model):
    TYPE_CHOICES = (
        ('PP', 'Private Practice'),
        ('SP', 'Small Practice'),
        ('C', 'Clinic')
    )
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    organisation_name = models.CharField(max_length=150)
    organisation_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    contacts = models.JSONField(default=dict)

    REQUIRED_FIELDS = ('organisation_name', 'organisation_type')

    def __str__(self):
        return self.organisation_name

class Administrator(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
