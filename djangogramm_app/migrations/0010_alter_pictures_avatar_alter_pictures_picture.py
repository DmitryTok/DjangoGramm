# Generated by Django 4.1.7 on 2023-06-07 18:17

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangogramm_app', '0009_alter_post_pictures'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pictures',
            name='avatar',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='pictures',
            name='picture',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, verbose_name='image'),
        ),
    ]
