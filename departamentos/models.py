from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from produtos.models import Produto


class Loja(models.Model):
    nome = models.CharField(verbose_name='Loja', max_length=50, unique=True)
    ativo = models.BooleanField(verbose_name='Ativo', default=True)
    created = models.DateTimeField(verbose_name='Criado em', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Atualizado em', auto_now=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Loja'
        verbose_name_plural = 'Lojas'


class Departamento(models.Model):
    nome = models.CharField(verbose_name='Departamento', max_length=50)
    slug = models.SlugField(verbose_name='Slug')
    ativo = models.BooleanField(verbose_name='Ativo', default=True)
    created = models.DateTimeField(verbose_name='Criado em', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Atualizado em', auto_now=True)
    produto = models.ManyToManyField(Produto, verbose_name='Produto', related_name='produtos',
                                     limit_choices_to={'ativo': True}, blank=True)
    loja = models.ForeignKey(Loja, verbose_name='Loja', on_delete=models.PROTECT, related_name='lojas',
                             limit_choices_to={'ativo': True})
    quantidade = models.FloatField(verbose_name='Qtd', default=0)

    class Meta:
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'
        ordering = ['loja']
        unique_together = ['nome', 'loja']

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse('departamento:detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = self.slug or slugify(self.nome)
        super().save(*args, **kwargs)
