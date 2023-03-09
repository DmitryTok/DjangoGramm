from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField()


class Avatar(models.Model):
    picture = models.ImageField(upload_to='profile/image')

    class Meta:
        ordering = ('id',)


class Post(models.Model):
    text = models.TextField(max_length=3000)
    post_picture = models.ImageField(upload_to='posts/image')
