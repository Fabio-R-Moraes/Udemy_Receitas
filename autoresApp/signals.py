from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from autoresApp.models import Profile

User = get_user_model()

@receiver(post_save, sender=User)
def criar_perfil(sender, instance, created, *args, **kwargs):
    print('Signal chamado:', instance.username, created)
    if created:
        perfil = Profile.objects.create(autor=instance)
        perfil.save()
