from django.db.models.signals import pre_save, post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver

from .models import Profile

User = get_user_model()


# Create your models here.
@receiver(post_save, sender=User)
def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        user_profile = Profile(user=user, email=user)
        user_profile.save()
        # group = Group.objects.get(name='simple_user')
        # user.groups.add(group)
        # user_profile.save()
