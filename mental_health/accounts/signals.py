from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.conf import settings

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


def send_verification_email(user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    verification_link = reverse('email_verify', kwargs={'uidb64': uid, 'token': token})
    full_link = f"{settings.SITE_URL}{verification_link}"

    subject = "Verify Your Email Address"
    message = render_to_string('accounts/email_verification.html', {'user': user, 'link': full_link})
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])