# Generated by Django 3.0.6 on 2020-05-09 20:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_profile_favorites'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='follows',
            new_name='following',
        ),
    ]