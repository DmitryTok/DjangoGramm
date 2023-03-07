from django.db import models


class Avatar(models.Model):
    picture = models.ImageField(upload_to='image')

    class Meta:
        ordering = ('id',)
