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
        related_name='post_tag'
    )
    likes = models.ManyToManyField(
        User,
        related_name='post_likes',
        blank=True
    )

    def likes_count(self):
        return self.likes.count()

    def __str__(self):
        return self.text
