# Generated by Django 4.1.7 on 2023-04-06 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_user_bio_user_name_alter_user_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='avatars.svg', null=True, upload_to=''),
        ),
    ]