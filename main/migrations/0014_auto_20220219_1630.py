# Generated by Django 3.1 on 2022-02-19 10:30

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0013_auto_20220219_1624'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='film',
            name='likes',
        ),
        migrations.AddField(
            model_name='comment',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='likers', to=settings.AUTH_USER_MODEL),
        ),
    ]
