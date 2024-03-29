# Generated by Django 4.1.7 on 2023-04-14 18:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('djangogramm_app', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='post_likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='post',
            name='pictures',
            field=models.ManyToManyField(blank=True, related_name='post_picture', to='djangogramm_app.pictures'),
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='post_tag', to='djangogramm_app.tag'),
        ),
        migrations.AddField(
            model_name='post',
            name='user',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name='post_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
