from django.shortcuts import render, redirect 
from .models import MoodEntry
from .forms import MoodEntryForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from textblob import TextBlob

def home(request):
    return render(request, 'tracker/home.html')


@login_required
def mood_tracker(request):
    if request.method == 'POST':
        form = MoodEntryForm(request.POST)
        if form.is_valid():
            mood_entry = form.save(commit=False)
            mood_entry.user = request.user
            if mood_entry.description:
                mood_entry.sentiment = analyze_sentiment(mood_entry.description)
            mood_entry.save()
            return redirect('mood_tracker')
    else:
        form = MoodEntryForm()
    
    moods = MoodEntry.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'tracker/mood_tracker.html', {'form': form, 'moods': moods})


@login_required
def mood_data(request):
    moods = MoodEntry.objects.filter(user=request.user).order_by('timestamp')
    data = {
        'dates': [mood.timestamp.strftime('%Y-%m-%d') for mood in moods],
        'moods': [mood.mood for mood in moods],
        'sentiments': [mood.sentiment for mood in moods],
    }
    return JsonResponse(data)


@login_required
def dashboard(request):
    return render(request, 'accounts/dashboard.html')  # Renders the dashboard page
    

def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0:
        return 'positive'
    elif polarity < 0:
        return 'negative'
    else:
        return 'neutral'
