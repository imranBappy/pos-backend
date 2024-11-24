# models.py
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from apps.base.models import BaseModelWithoutID
from django.conf import settings


class GenderChoices(models.TextChoices):
    MALE = 'Male', 'Male'
    FEMALE = 'Female', 'Female'
    OTHER = 'Other', 'Other'

class UserRole(models.TextChoices):
    ADMIN = 'ADMIN', 'Admin'
    MANAGER = 'MANAGER', 'Manager'
    CHEF = 'CHEF', 'Chef'
    WAITER = 'WAITER', 'Waiter'
    CUSTOMER = 'CUSTOMER', 'Customer'


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
    
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None

class User(BaseModelWithoutID, AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    term_and_condition_accepted = models.BooleanField(default=False)
    privacy_policy_accepted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    gender = models.CharField(max_length=8, choices=GenderChoices.choices, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.URLField(max_length=1000, blank=True, null=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  # Avoids conflict with default reverse relationship
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',  # Avoids conflict with default reverse relationship
        blank=True
    )


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

        
    def __str__(self):
        return f"{self.id} - {self.name}"
