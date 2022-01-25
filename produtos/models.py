import re

from django.core.validators import MaxValueValidator
from django.db import models

from lojas.models import Departamento, Loja, Area


class Unidade(models.Model):
    nome = models.CharField(verbose_name='Unidade', max_length=2)
    ativo = models.BooleanField(verbose_name='Ativo', default=True)

    class Meta:
        verbose_name = 'Unidade'
        verbose_name_plural = 'Unidades'

    def __str__(self):
        return self.nome


class Tipo(models.Model):
    nome = models.CharField(verbose_name='Tipo', max_length=50)
    ativo = models.BooleanField(verbose_name='Ativo', default=True)

    class Meta:
        verbose_name = 'Tipo'
        verbose_name_plural = 'Tipos'

    def __str__(self):
        return self.nome


class Lista(models.Model):
    nome = models.CharField(verbose_name='Lista de compras', max_length=50)
    # contagem = models.ManyToManyField(Contagem, verbose_name='Contagem', related_name='lista')
    created = models.DateTimeField(verbose_name='Criada em', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Atualizada em', auto_now=True)
    ativo = models.BooleanField(verbose_name='Ativo', default=True)

    class Meta:
        verbose_name = 'Lista'
        verbose_name_plural = 'Listas'

    def __str__(self):
        return self.nome


class Produto(models.Model):
    nome = models.CharField(verbose_name='Nome', max_length=50)
    tipo = models.ForeignKey(Tipo, verbose_name='Tipo', max_length=50, on_delete=models.PROTECT,
                             related_name='produtos')
    unidade = models.ForeignKey(Unidade, verbose_name='Unidade', max_length=2, on_delete=models.PROTECT)
    descricao = models.TextField(verbose_name='Descrição', blank=True)
    pesquisa = models.TextField(verbose_name='Conteúdo pesquisável', editable=False)
    loja = models.ForeignKey(Loja, verbose_name='Loja', related_name='produtos',
                             on_delete=models.PROTECT)
    departamento = models.ForeignKey(Departamento, verbose_name='Departamento', related_name='produtos',
                                     on_delete=models.PROTECT)
    lista = models.ForeignKey(Lista, verbose_name='Lista', related_name='produtos', on_delete=models.CASCADE)
    area = models.ForeignKey(Area, verbose_name='Área', on_delete=models.PROTECT, related_name='produtos')
    qtd = models.FloatField(verbose_name='Quantidade', default=0)
    media = models.IntegerField(verbose_name='Média', validators=[MaxValueValidator(10000)])
    comprar = models.FloatField(verbose_name='Comprar', blank=True, default=0, editable=False)
    ativo = models.BooleanField(verbose_name='Ativo', default=True)
    created = models.DateTimeField(verbose_name='Criado em', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['nome']
        unique_together = ('nome', 'loja')

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

    def calcula_comprar(self):
        if self.qtd > self.media:
            comprar = 0
        else:
            comprar = self.media - self.qtd
        return comprar

    def save(self, *args, **kwargs):
        self.pesquisa = self.formata_pesquisa()
        self.comprar = self.calcula_comprar()
        super().save(*args, **kwargs)


# class Contagem(models.Model):
#     produto = models.ForeignKey(Produto, verbose_name='Produto', on_delete=models.CASCADE, related_name='contagem')
#     qtd = models.FloatField(verbose_name='Quantidade', blank=True, default=0)
#     comprar = models.FloatField(verbose_name='Comprar', blank=True, default=0, editable=False)
#     created = models.DateTimeField(verbose_name='Criado em', auto_now_add=True)
#
#     class Meta:
#         verbose_name = 'Contagem'
#         verbose_name_plural = 'Contagens'
#         ordering = ['produto']
#
#     def get_produtos(self):
#         return "\n".join([p.nome for p in self.produto.all()])
#
#     def calcula_comprar(self):
#         if self.qtd > self.produto.media:
#             comprar = 0
#         else:
#             comprar = self.produto.media - self.qtd
#         return comprar
#
#     def save(self, *args, **kwargs):
#         self.comprar = self.calcula_comprar()
#         super().save(*args, **kwargs)
#
#     def __str__(self):
#         return self.produto.nome
