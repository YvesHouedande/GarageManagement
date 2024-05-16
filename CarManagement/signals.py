from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import EntreVehicule, EntrePanne


@receiver(post_save, sender=EntreVehicule)
def create_entre_panne(sender, instance, created, **kwargs):
    if created:
        for panne in instance.pannes.all():
            EntrePanne.objects.create(entre=instance, panne=panne)
