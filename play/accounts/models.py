from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field is required")
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to="profiles/", blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    term_and_condition_accepted = models.BooleanField(default=False)
    privacy_policy_accepted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Add this field
    is_deleted = models.BooleanField(default=False)
    gender = models.CharField(max_length=10, choices=(('Male', 'Male'), ('Female', 'Female')), null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    
    # Fields for role-based access
    groups = models.ManyToManyField(Group, related_name='users')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
   
    objects = UserManager()

    def __str__(self):
        return self.email
