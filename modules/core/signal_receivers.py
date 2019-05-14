from django.db.models.signals import post_save
from django.dispatch import receiver
from modules.core.models import *


@receiver(post_save, sender=Channel)
def post_save_channel(instance, *args, **kwargs):
    if instance.main_channel:
        Channel.objects.filter(id_channel=instance.id_channel).exclude(pk=instance.pk).update(main_channel=False)
