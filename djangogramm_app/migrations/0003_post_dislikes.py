# Generated by Django 4.1.7 on 2023-04-15 10:33

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('djangogramm_app', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='dislikes',
            field=models.ManyToManyField(blank=True, related_name='post_dislikes', to=settings.AUTH_USER_MODEL),
        ),
    ]
