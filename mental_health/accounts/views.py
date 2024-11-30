from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import ProfileForm, CustomUserCreationForm
from .models import Profile
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from datetime import timedelta
from django.utils.timezone import now
from django.db.models import Count
from tracker.models import MoodEntry  
from textblob import TextBlob

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Set user as inactive until they verify their email
            user.save()
            
            # Generate email verification token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Create email verification link
            verification_link = f"{settings.SITE_URL}/verify-email/{uid}/{token}/"
            
            # Send verification email
            subject = "Verify Your Email Address"
            message = render_to_string('accounts/email_verification.html', {
                'user': user,
                'verification_link': verification_link,
            })
            send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])

            messages.success(request, 'Account created successfully! Please check your email to verify your account.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})

    
    
    

@csrf_protect  # Ensure CSRF protection is enabled for this view
def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect to the dashboard
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    messages.info(request, 'Logged out successfully.')
    return redirect('login')

@login_required
def profile_edit(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully")
            return redirect('profile_view')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'accounts/profile_edit.html', {'form': form})

@login_required
def profile_view(request):
    return render(request, 'accounts/profile_view.html', {'user': request.user})


User = get_user_model()

def verify_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse("Your email has been verified successfully! You can now log in.")
    else:
        return HttpResponse("Verification link is invalid or expired.")
    
    
def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0:
        return 'positive'
    elif polarity < 0:
        return 'negative'
    else:
        return 'neutral'
    

@login_required
def dashboard(request):
    # Generate mood insights for the logged-in user
    insights = generate_mood_insights(request.user)
    return render(request, 'accounts/dashboard.html', {'insights': insights})

def generate_mood_insights(user):
    # Define a time range for the past week
    one_week_ago = now() - timedelta(days=7)

    # Query mood entries from the past week
    moods = MoodEntry.objects.filter(user=user, timestamp__gte=one_week_ago)

    # If no mood data exists, return a default message
    if not moods.exists():
        return "No mood data available for insights. Start logging your moods!"

    # Analyze mood data
    mood_count = moods.count()
    mood_summary = moods.values('mood').annotate(count=Count('mood')).order_by('-count')
    mood_polarities = [analyze_sentiment(mood.description) for mood in moods]

    # Calculate positive and negative sentiment counts
    positive_count = mood_polarities.count('positive')
    negative_count = mood_polarities.count('negative')

    # Generate insights based on mood analysis
    if positive_count > negative_count:
        return f"In the past week, {positive_count} out of {mood_count} moods were positive. Keep up the good vibes!"
    elif negative_count > positive_count:
        return f"It seems {negative_count} out of {mood_count} moods were negative. Consider self-care or seeking support."
    else:
        return "Your mood trend has been neutral. A bit of positivity could brighten your week!"
