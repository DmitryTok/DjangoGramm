# Generated by Django 4.1.7 on 2023-03-08 12:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangogramm_app', '0004_initial'),
        ('users', '0002_remove_user_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='djangogramm_app.avatar'),
        ),
    ]
