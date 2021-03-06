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
        permissions = (
            ('fabrica', 'Pode acessar fabrica'),
            ('marista', 'Pode acessar marista'),
            ('passeio', 'Pode acessar passeio'),
        )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nome)
        super().save(*args, **kwargs)


class Departamento(models.Model):
    nome = models.CharField(verbose_name='Departamento', max_length=50)
    slug = models.SlugField(verbose_name='Slug', editable=False)
    ativo = models.BooleanField(verbose_name='Ativo', default=True)
    loja = models.ForeignKey(Loja, verbose_name='Loja', on_delete=models.PROTECT, related_name='departamentos',
                             limit_choices_to={'ativo': True})

    class Meta:
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'
        ordering = ['loja']
        unique_together = ['nome', 'loja']
        permissions = (
            ('cozinha marista', 'Pode acessar cozinha do marista'),
            ('bar marista', 'Pode acessar bar do marista'),
            ('demais marista', 'Pode acessar demais do marista'),
            ('cozinha passeio', 'Pode acessar cozinha do passeio'),
            ('bar passeio', 'Pode acessar bar do passeio'),
            ('demais passeio', 'Pode acessar demais do passeio'),
            
        )

    def __str__(self):
        return f'{self.loja} - {self.nome}'

    def get_absolute_url(self):
        return reverse('departamento:detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nome)
        super().save(*args, **kwargs)


class Area(models.Model):
    nome = models.CharField(verbose_name='??rea', max_length=20)
    slug = models.SlugField(verbose_name='Slug', editable=False)
    departamento = models.ForeignKey(Departamento, verbose_name='Departamento', on_delete=models.PROTECT,
                                     related_name='areas')
    cor = models.CharField(verbose_name='Cor', max_length=7)
    ativo = models.BooleanField(verbose_name='Ativo', default=True)

    class Meta:
        verbose_name = '??rea'
        verbose_name_plural = '??reas'

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nome)
        super().save(*args, **kwargs)
