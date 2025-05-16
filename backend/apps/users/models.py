import uuid

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self, email, username, description, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address.')
        if not username:
            username = email.split('@')[0]
        if not description:
            description = ''

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            description=description,
            is_active=True,
            **extra_fields,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Superusers must have an email address.')
        if password is None:
            raise ValueError('Superusers must have a password.')

        username = email.split('@')[0]
        description = ''

        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            description=description,
            password=password,
            **extra_fields
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=32, unique=True, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    avatar = models.ImageField(upload_to='static/avatars/', null=True, blank=True, default='static/avatars/default_avatar.black.png')

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.username or self.email or str(self.id)

    def has_perm(self, perm, obj=None):
        return self.is_active and self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_active and self.is_staff


class ActivationCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_expired(self):
        return timezone.now() > self.expires_at
