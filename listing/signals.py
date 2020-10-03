from django.db.models.constraints import UniqueConstraint
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify

from .models import Listing


@receiver(post_save, sender=Listing)
def slug_generator(sender, instance, *args, **kwargs):
    """
    Signal that creates a slug for a model instance whenever it's needed
    """
    if instance.slug:
        return
    instance.slug = slugify(f'{instance.name}-{instance.id}')
    instance.save()