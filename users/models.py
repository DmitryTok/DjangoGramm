from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(
        _('email address'),
        unique=True,
    )
    full_name = models.CharField(max_length=50)
    bio = models.TextField(max_length=1500)
    avatar = models.ImageField(
        upload_to='avatars/',
        null=True,
        blank=True
    )
    is_email_veryfi = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('email', 'username'),
                name='unique_username_email')
        ]

    def __str__(self):
        return self.email
