from accounts.models import CustomUser, Profile
from django.db.models.signals import post_save
from django.dispatch import receiver
from multi_user.models import Collaboration
from targets.models import Saving


@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        Saving.objects.create(user=instance)
        Collaboration.objects.create(user=instance)
