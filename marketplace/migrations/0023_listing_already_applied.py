# Generated by Django 3.1.9 on 2021-06-02 17:28

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('marketplace', '0022_remove_listing_confirmed_and_awaiting'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='already_applied',
            field=models.ManyToManyField(blank=True, related_name='already_applied', to=settings.AUTH_USER_MODEL),
        ),
    ]