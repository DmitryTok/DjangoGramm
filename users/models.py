from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


# delete migrations: python3 manage.py migrate users zero
class User(AbstractUser):
    email = models.EmailField(
        _('email address'),
        blank=False,
        null=False,
        unique=True
    )
    full_name = models.CharField(max_length=20, null=True)
    bio = models.TextField(max_length=1500, null=True)
    is_email_verify = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('email',),
                name='unique_email')
        ]

    def __str__(self):
        return self.email
