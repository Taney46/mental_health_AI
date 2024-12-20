# Generated by Django 5.1.3 on 2024-11-29 16:22

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='moodentry',
            old_name='note',
            new_name='description',
        ),
        migrations.RemoveField(
            model_name='moodentry',
            name='date',
        ),
        migrations.AddField(
            model_name='moodentry',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
        model_name='moodentry',
        name='user',
        field=models.ForeignKey(
            to=settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE,
            null=True,  # Allow null values temporarily
            blank=True,
        ),
    )
    ]