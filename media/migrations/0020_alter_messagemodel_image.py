# Generated by Django 4.1 on 2022-09-20 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0019_alter_messagemodel_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messagemodel',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='chat_images'),
        ),
    ]
