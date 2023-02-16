from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models


class Picture(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ImageField()

    class Meta:
        ordering = ('id',)
        verbose_name = 'Image'
        verbose_name_plural = 'Images'

    def __str__(self):
        return self.image


class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=15)
    slug = models.SlugField()

    class Meta:
        ordering = ('id',)
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.name


class DGUser(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True, null=False)
    password = models.CharField(max_length=16, unique=True, null=False)
    full_name = models.CharField(max_length=50, null=True, blank=True)
    bio = models.TextField(max_length=500, null=True, blank=True)
    email_verify = models.BooleanField(default=False)
    avatar = models.ForeignKey(
        Picture,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'password']

    class Meta:
        ordering = ('-id',)
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        constraints = [
            models.UniqueConstraint(
                fields=['email'],
                name='unique_email'
            )
        ]

    def __str__(self):
        return f'{self.full_name}'


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField(max_length=5000)
    tags = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    image = models.ForeignKey(
        Picture,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return self.text


class PostTag(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    tag_id = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        ordering = ('post_id',)
        verbose_name = 'Post tag'
        verbose_name_plural = 'Posts tags'
        constraints = [
            models.UniqueConstraint(
                fields=['post_id', 'tag_id'],
                name='unique_post_tag'
            )
        ]

    def __str__(self):
        return f'{self.post_id}: {self.tag_id}'


class Like(models.Model):
    user_id = models.ForeignKey(
        DGUser,
        on_delete=models.CASCADE,
    )
    post_id = models.ForeignKey(
        Post,
        on_delete=models.CASCADE
    )
    is_like = models.BooleanField(default=None)

    class Meta:
        ordering = ('post_id',)
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'
        constraints = [
            models.UniqueConstraint(
                fields=['user_id', 'post_id'],
                name='unique_user_post'
            )
        ]

    def __str__(self):
        return f'{self.user_id}: {self.post_id}'
