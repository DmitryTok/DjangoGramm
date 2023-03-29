from django.db import models

from users.models import User


class Tag(models.Model):
    name = models.CharField(
        max_length=50,
    )

    def __str__(self):
        return self.name


class Post(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='post_user'
    )
    text = models.TextField(max_length=2000)
    picture = models.ImageField(upload_to='post_image/', blank=True, null=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        null=True,
        related_name='post_tag'
    )

    def __str__(self):
        return self.text
