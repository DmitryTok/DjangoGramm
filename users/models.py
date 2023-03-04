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
    bio = models.TextField(max_length=1500)
    is_email_verify = models.BooleanField(default=False)
    # TODO avatar = ForeignKey(Avatar, on_delete=models.CASCADE, blank=True, null=True, unique=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('email',),
                name='unique_email')
        ]

    def __str__(self):
        return self.email
