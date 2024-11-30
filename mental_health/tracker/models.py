from django.db import models
from django.contrib.auth.models import User

class MoodEntry(models.Model):
    MOOD_CHOICES = [
        ('happy', 'Happy'),
        ('neutral', 'Neutral'),
        ('sad', 'Sad'),
        ('angry', 'Angry'),
        ('excited', 'Excited'),
        ('anxious', 'Anxious'),
        # Add more moods if needed
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mood_entries')
    mood = models.CharField(max_length=50, choices=MOOD_CHOICES)
    description = models.TextField(blank=True, null=True)  # Optional field for user notes
    sentiment = models.CharField(max_length=10, choices=[('positive', 'Positive'), ('neutral', 'Neutral'), ('negative', 'Negative')])
    timestamp = models.DateTimeField(auto_now_add=True)  # Automatically set when created

    def __str__(self):
        return f"{self.user.username} - {self.mood} ({self.timestamp.strftime('%Y-%m-%d %H:%M:%S')})"
