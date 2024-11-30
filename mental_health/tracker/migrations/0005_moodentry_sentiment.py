# Generated by Django 5.1.3 on 2024-11-30 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0004_alter_moodentry_description_alter_moodentry_mood_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='moodentry',
            name='sentiment',
            field=models.CharField(choices=[('positive', 'Positive'), ('neutral', 'Neutral'), ('negative', 'Negative')], default='neutral', max_length=10),
        ),
    ]