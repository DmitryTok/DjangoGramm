from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from djangogramm_app.models import Pictures


class User(AbstractUser):
    email = models.EmailField(
        _('email address'),
        unique=True,
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[UnicodeUsernameValidator()]
    )
    full_name = models.CharField(max_length=50)
    bio = models.TextField(max_length=1500)
    avatar = models.ForeignKey(
        Pictures,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    is_email_verify = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('email', 'username'),
                name='unique_username_email')
        ]

    def __str__(self):
        return f'{self.email}'


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followed_by'
    )

    def __str__(self):
        return f'{self.user} follows {self.author}'
