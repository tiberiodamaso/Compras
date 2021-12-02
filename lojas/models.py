from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Loja(models.Model):
    nome = models.CharField(verbose_name='Loja', max_length=50, unique=True)
    slug = models.SlugField(verbose_name='Slug', editable=False)
    ativo = models.BooleanField(verbose_name='Ativo', default=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Loja'
        verbose_name_plural = 'Lojas'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nome)
        super().save(*args, **kwargs)


class Departamento(models.Model):
    nome = models.CharField(verbose_name='Departamento', max_length=50)
    slug = models.SlugField(verbose_name='Slug', editable=False)
    ativo = models.BooleanField(verbose_name='Ativo', default=True)
    loja = models.ForeignKey(Loja, verbose_name='Loja', on_delete=models.PROTECT, related_name='lojas',
                             limit_choices_to={'ativo': True})

    class Meta:
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'
        ordering = ['loja']
        unique_together = ['nome', 'loja']

    def __str__(self):
        return f'{self.nome}'

    def get_absolute_url(self):
        return reverse('departamento:detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nome)
        super().save(*args, **kwargs)
