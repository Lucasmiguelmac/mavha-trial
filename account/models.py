from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from hashid_field import HashidAutoField
from .managers import UserManager


class User(AbstractBaseUser):
    """
    Django's user model overwritten to achieve desired fields.
    """
    id      = HashidAutoField(primary_key=True)
    name    = models.CharField(max_length=35)
    email   = models.EmailField(max_length=60, unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def __str__(self) -> str:
        return self.email