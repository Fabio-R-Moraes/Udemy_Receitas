from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from django.db.models import F, Value
from django.db.models.functions import Concat
from tagApp.models import Tag
from django.forms import ValidationError
from collections import defaultdict
from django.utils.translation import gettext_lazy as _

class ReceitasManager(models.Manager):
    def get_publicados(self):
        return self.filter(
            esta_publicado=True,
        ).annotate(
        autor_nome_completo=Concat(
            F('autor__first_name'),
            Value(' '),
            F('autor__last_name'),
            Value(' ('),
            F('autor__username'),
            Value(')')
        )
    ).order_by('-id')

class Categoria(models.Model):
    nome = models.CharField(max_length=65)

    def __str__(self):
        return self.nome

class Receitas(models.Model):
    objects = ReceitasManager()
    titulo = models.CharField(max_length=65, verbose_name=_('Title'))
    descricao = models.CharField(max_length=165, verbose_name=_('Description'))
    slug = models.SlugField(unique=True)
    tempo_preparo = models.IntegerField()
    unidade_tempo_preparo = models.CharField(max_length=65)
    porcoes = models.IntegerField()
    unidade_porcoes = models.CharField(max_length=65)
    modo_preparo = models.TextField()
    modo_preparo_html = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    esta_publicado = models.BooleanField(default=False)
    receita_imagem = models.ImageField(upload_to='receitas/receitas_imagens/%d/%m/%Y/',
                      blank=True, default=''
                      )
    categoria = models.ForeignKey(
        Categoria, on_delete=models.SET_NULL, null=True, blank=True,
        default=None
    )
    autor = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True
    )
    tags = models.ManyToManyField(Tag, blank=True, default='')

    def __str__(self):
        return self.titulo

    def get_abolute_url(self):
        return reverse('receitas:receita', args=(self.id,))

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.titulo)}'
            self.slug = slug

        return super().save(*args, **kwargs)

    def clean(self, *args, **kwargs):
        error_message = defaultdict(list)
        receitas_do_bd = Receitas.objects.filter(
            titulo__iexact = self.titulo
        ).first()

        if receitas_do_bd:
            if receitas_do_bd.pk != self.pk:
                error_message['titulo'].append(
                    'Encontrei receitas com esse mesmo título!!!'
                )

        if error_message:
            raise ValidationError(error_message)

    class Meta:
        verbose_name = _('Recipe')
        verbose_name_plural = _('Recipes')
