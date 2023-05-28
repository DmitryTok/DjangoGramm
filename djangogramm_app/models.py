from django.db import models


class Pictures(models.Model):
    picture = models.ImageField(upload_to='pictures', max_length=300)

    def __str__(self):
        return f'Image {self.picture}'


class Tag(models.Model):
    name = models.CharField(
        max_length=300,
    )

    def __str__(self):
        return self.name


class Post(models.Model):
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='post_user'
    )
    text = models.TextField(max_length=2000)
    pictures = models.ManyToManyField(
        Pictures,
        blank=True,
        related_name='post_picture'
    )
    pub_date = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='post_tag'
    )
    likes = models.ManyToManyField(
        'users.User',
        related_name='post_likes',
        blank=True
    )
    dislikes = models.ManyToManyField(
        'users.User',
        related_name='post_dislikes',
        blank=True
    )

    def likes_count(self):
        return self.likes.count()

    def dislikes_count(self):
        return self.dislikes.count()

    def __str__(self):
        return self.text
