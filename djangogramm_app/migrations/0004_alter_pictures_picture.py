# Generated by Django 4.1.7 on 2023-05-28 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangogramm_app', '0003_post_dislikes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pictures',
            name='picture',
            field=models.ImageField(max_length=300, upload_to='pictures'),
        ),
    ]
