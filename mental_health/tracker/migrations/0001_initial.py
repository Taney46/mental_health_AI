# Generated by Django 5.1.3 on 2024-11-29 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MoodEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('mood', models.CharField(max_length=100)),
                ('note', models.TextField(blank=True)),
            ],
        ),
    ]
