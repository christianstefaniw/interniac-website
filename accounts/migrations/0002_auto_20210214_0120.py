# Generated by Django 3.1.6 on 2021-02-14 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employerprofile',
            name='profile_picture',
        ),
        migrations.RemoveField(
            model_name='studentprofile',
            name='profile_picture',
        ),
        migrations.AddField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pictures'),
        ),
    ]
