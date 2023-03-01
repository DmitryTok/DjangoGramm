from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(
        _('email  adress'),
        blank=False,
        null=False,
        unique=True
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
