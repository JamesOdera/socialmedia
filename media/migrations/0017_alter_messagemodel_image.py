# Generated by Django 4.1 on 2022-09-20 09:00

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0016_alter_messagemodel_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messagemodel',
            name='image',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image'),
        ),
    ]
