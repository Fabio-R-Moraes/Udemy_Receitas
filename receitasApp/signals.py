import os
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from receitasApp.models import Receitas

def delete_imagem(instance):
    try:
        os.remove(instance.receita_imagem.path)
    except (ValueError, FileNotFoundError) as e:
        print(e)

@receiver(pre_delete, sender=Receitas)
def receita_imagem_deletar(sender, instance, *args, **kwargs):
    print('SIGNAL CHAMADO PELA RECEITA...')
    old_instance = Receitas.objects.filter(pk=instance.pk).first()
    delete_imagem(old_instance)

@receiver(pre_save, sender=Receitas)
def receita_imagem_update(sender, instance, *args, **kwargs):
    old_instance = Receitas.objects.filter(pk=instance.pk).first()
    print(old_instance.receita_imagem, instance.receita_imagem)
    nova_imagem = old_instance.receita_imagem != instance.receita_imagem
    print('Troquei a imagem??', nova_imagem)

    if nova_imagem:
        delete_imagem(old_instance)
