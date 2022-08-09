from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
import os

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

@receiver(pre_save, sender=Profile)
def auto_delete_image_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_image = Profile.objects.get(pk=instance.pk).image
    except Profile.DoesNotExist:
        return False
    new_image = instance.image
    if not old_image == new_image and 'default.png' not in old_image.path:
        if os.path.isfile(old_image.path):
            os.remove(old_image.path)
