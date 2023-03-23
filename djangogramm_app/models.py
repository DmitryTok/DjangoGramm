from django.db import models

from users.models import User


class Post(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='post_user'
    )
    text = models.TextField(max_length=2000)
    picture = models.ImageField(upload_to='post_image/', blank=True, null=True)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
