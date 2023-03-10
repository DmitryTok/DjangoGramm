from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Avatar(models.Model):
    picture = models.ImageField(upload_to='images/')


class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField()


class Post(models.Model):
    title = models.CharField(max_length=25)
    text = models.TextField(max_length=3000)
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    post_picture = models.ForeignKey(
        Avatar,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )


class PostTag(models.Model):
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('post', 'tag'),
                name='unique_post_tag')
        ]


class Like(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    is_liked = models.BooleanField(default=None)
