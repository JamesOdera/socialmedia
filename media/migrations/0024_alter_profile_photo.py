# Generated by Django 4.1 on 2022-10-07 13:00

import cloudinary.models
from django.db import migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0023_alter_profile_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=cloudinary.models.CloudinaryField(default=django.utils.timezone.now, max_length=255, verbose_name='image-profile'),
            preserve_default=False,
        ),
    ]
