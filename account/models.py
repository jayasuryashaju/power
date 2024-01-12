import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

def validate_password(value):
    if not any(char.isdigit() for char in value):
        raise ValidationError(_('The password must contain at least one digit.'))
    if not any(char.isalpha() for char in value):
        raise ValidationError(_('The password must contain at least one letter.'))
    if not any(not char.isalnum() for char in value):
        raise ValidationError(_('The password must contain at least one special character.'))

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, full_name, phone_number, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, full_name=full_name, phone_number=phone_number, **extra_fields)
        user.set_password(password)  # This line hashes the password
        user.full_clean()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, full_name, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, full_name, phone_number, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        primary_key=True
    )
    
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    full_name = models.CharField(max_length=60)
    phone_number = models.CharField(max_length=15, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'full_name', 'phone_number']

    password = models.CharField(
        max_length=128,
        validators=[
            MinLengthValidator(8),
            validate_password,
        ]
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name
