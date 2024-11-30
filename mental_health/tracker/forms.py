from django import forms
from .models import MoodEntry

class MoodEntryForm(forms.ModelForm):
    """
    Form for users to log mood entries.
    """
    class Meta:
        model = MoodEntry
        fields = ['mood', 'description']  # Fields to include in the form
        widgets = {
            'mood': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
