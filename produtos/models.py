import re

from django.db import models
from django.utils.text import slugify

from lojas.models import Departamento, Loja


def path_to_upload(produto, filename):
    extensao = filename.split('.')[1]
    return f'produtos/{slugify(produto.nome)}.{extensao}'


class Unidade(models.Model):
    nome = models.CharField(verbose_name='Unidade', max_length=2)
    ativo = models.BooleanField(verbose_name='Ativo', default=True)

    class Meta:
        verbose_name = 'Unidade'
        verbose_name_plural = 'Unidades'

    def __str__(self):
        return self.nome


class Lista(models.Model):
    nome = models.CharField(verbose_name='Lista de compras', max_length=50)
    ativo = models.BooleanField(verbose_name='Ativo', default=True)

    class Meta:
        verbose_name = 'Lista'
        verbose_name_plural = 'Listas'

    def __str__(self):
        return self.nome


# Create your models here.
class Produto(models.Model):
    nome = models.CharField(verbose_name='Nome', max_length=50)
    lista = models.ForeignKey(Lista, verbose_name='Lista de compras', max_length=50, on_delete=models.PROTECT)
    unidade = models.ForeignKey(Unidade, verbose_name='Unidade', max_length=2, on_delete=models.PROTECT)
    imagem = models.ImageField(verbose_name='Imagem', upload_to=path_to_upload, blank=True)
    descricao = models.TextField(verbose_name='Descrição', blank=True)
    pesquisa = models.TextField(verbose_name='Conteúdo pesquisável')
    departamento = models.ForeignKey(Departamento, verbose_name='Departamento', related_name='produtos',
                                     on_delete=models.PROTECT)
    loja = models.ForeignKey(Loja, verbose_name='Loja', related_name='produtos',
                             on_delete=models.PROTECT)
    qtd = models.FloatField(verbose_name='Quantidade', blank=True, default=0)
    ativo = models.BooleanField(verbose_name='Ativo', default=True)
    created = models.DateTimeField(verbose_name='Criado em', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['nome']

    def __str__(self):
        return self.nome

    def formata_pesquisa(self):
        pesquisa = self.nome.lower() + self.descricao.lower()

        # substituir caracteres acentuados por não acentuados
        pesquisa = re.sub(r'[áàâãä]', 'a', pesquisa)
        pesquisa = re.sub(r'[éèêë]', 'e', pesquisa)
        pesquisa = re.sub(r'[íìîï]', 'i', pesquisa)
        pesquisa = re.sub(r'[óòôõö]', 'o', pesquisa)
        pesquisa = re.sub(r'[úùûü]', 'u', pesquisa)
        pesquisa = re.sub('ç', 'c', pesquisa)

        # remover todos os caracteres que não são números e não são letras (caracter de linha, de parágrafo etc)
        pesquisa = re.sub(r'[^a-z0-9]', '', pesquisa)

        return pesquisa

    def save(self, *args, **kwargs):
        self.pesquisa = self.formata_pesquisa()
        super().save(*args, **kwargs)
