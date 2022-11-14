from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin)
from django.utils.translation import gettext_lazy as _


# from .managers import UserManager

# CREATE CUSTOM USER MANAGER
class UserManager(BaseUserManager):
    def _create_user(self, email, password, is_admin, is_superuser, **extra_fields):
        """
        Creates and saves a User using helper function.
        """
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            is_admin=is_admin,
            is_superuser=is_superuser,
            last_login=timezone.now(),
            date_joined=timezone.now(),
        )
        # set the user password
        user.set_password(password)
        user.save(using=self._db)
        return user

    # create simple user
    def create_user(self, email, password, **extra_fields):
        """
        Creates and saves a user with the given username, email, and password.
        """
        user = self._create_user(email, password, False, False, **extra_fields)
        return user

    # create superuser
    def create_superuser(self, email, password, **extra_fields):
        """
        Creates and saves a superuser with the given username, email, and password.
        """
        user = self._create_user(email, password, True, True, **extra_fields)
        user.is_superuser = True
        user.is_admin = True
        return user


#  class create custom user model with email
# like primary login field


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True, db_index=True, verbose_name='email address')
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    # override the default object manager and using UserManager
    objects = UserManager()

    # use email like first auth field (override the default username)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.email

    def get_full_name(self):
        """Return the email."""
        return self.email

    def get_short_name(self):
        """Return the email."""
        return self.email

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        # Simplest possible answer: All admins are staff
        return self.is_admin

    # @property
    # def is_active(self):
    #     """if user is active """
    #     return self.is__active
