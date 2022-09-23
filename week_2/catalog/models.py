from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager


class CustomAccountManager(BaseUserManager):
    def create_user(self, username, fullname, email, password):
        user = self.model(email=email, username=username, fullname=fullname, password=password)
        user.set_password(password)
        user.is_staff = False
        user.is_superuser = False
        user.save(using=self._db)
        return user

    def create_superuser(self, username, fullname, email, password):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        if not fullname:
            raise ValueError("User must have a full name")
        user = self.model(email=email, username=username, fullname=fullname, password=password)
        user.set_password(password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, username_):
        return self.get(username=username_)


class AdvUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=200, unique=True)
    fullname = models.CharField(max_length=200)
    email = models.EmailField(unique=True, max_length=200)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['fullname', 'password', 'email']

    objects = CustomAccountManager()

    def get_short_name(self):
        return self.username

    def natural_key(self):
        return self.username

    def __str__(self):
        return self.username
