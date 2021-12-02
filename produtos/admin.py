from django.contrib import admin

# Register your models here.
from produtos.models import Produto, Unidade, Lista


class UnidadeAdmin(admin.ModelAdmin):
    list_display = ['nome', 'ativo']
    list_filter = ['nome', 'ativo']
    search_fields = ['nome']


class ListaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'ativo']
    list_filter = ['nome', 'ativo']
    search_fields = ['nome']


class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'loja', 'departamento', 'lista', 'qtd']
    list_filter = ['nome', 'loja', 'departamento', 'lista']
    search_fields = ['nome', 'lista']


admin.site.register(Unidade, UnidadeAdmin)
admin.site.register(Lista, ListaAdmin)
admin.site.register(Produto, ProdutoAdmin)
