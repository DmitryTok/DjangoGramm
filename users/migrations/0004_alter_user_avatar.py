# Generated by Django 4.1.7 on 2023-06-07 18:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangogramm_app', '0011_alter_post_pictures'),
        ('users', '0003_follow'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ForeignKey(
                blank=True, on_delete=django.db.models.deletion.CASCADE, to='djangogramm_app.pictures'),
        ),
    ]
