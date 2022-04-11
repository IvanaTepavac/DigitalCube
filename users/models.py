from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager


class Users(AbstractBaseUser, PermissionsMixin):
    """
    Extended User model, stores Users data
    """

    full_name = models.CharField('Full name', max_length=80)
    email = models.EmailField('Email', blank=False, unique=True)
    username = models.CharField('Username', max_length=50, blank=False, unique=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"

    def __str__(self):
        return f"{self.full_name}"

    class Meta:
        db_table = 'users'
