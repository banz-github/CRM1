from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(user_logged_in, sender=User)
def update_last_login(sender, request, user, **kwargs):
    user.save(update_fields=['last_login'])
