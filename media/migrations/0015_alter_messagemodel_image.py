# Generated by Django 4.1 on 2022-09-20 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0014_alter_post_options_remove_post_shared_body_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messagemodel',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='chat_images'),
        ),
    ]
