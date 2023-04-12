# Generated by Django 4.1.7 on 2023-04-12 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangogramm_app', '0003_remove_post_picture_post_pictures'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='pictures',
            field=models.ManyToManyField(blank=True, related_name='post_picture', to='djangogramm_app.pictures'),
        ),
    ]