from django.db import models


class Avatar(models.Model):
    image = models.ImageField()
