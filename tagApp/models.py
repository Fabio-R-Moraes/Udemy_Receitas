from django.db import models
from django.utils.text import slugify
import string
from random import SystemRandom

class Tag(models.Model):
    nome = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            letras_randomicas = ''.join(
                SystemRandom().choices(
                    string.ascii_letters + string.digits,
                    k=5,
                )
            )
            self.slug = slugify(f'{self.nome}-{letras_randomicas}')

        return super().save(*args, **kwargs)
