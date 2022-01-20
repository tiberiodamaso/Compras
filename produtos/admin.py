from django.contrib import admin

# Register your models here.
from produtos.models import Produto, Unidade, Lista, Tipo


class UnidadeAdmin(admin.ModelAdmin):
    list_display = ['nome', 'ativo']
    list_filter = ['nome', 'ativo']
    search_fields = ['nome']


class ListaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'qtd', 'comprar', 'created', 'ativo']
    list_filter = ['nome', 'ativo']
    search_fields = ['nome']


class TipoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'ativo']
    list_filter = ['nome', 'ativo']
    search_fields = ['nome']


class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'loja', 'departamento', 'area', 'tipo', 'media', 'qtd']
    list_filter = ['nome', 'loja', 'departamento']
    search_fields = ['nome', 'lista']
    readonly_fields = ['pesquisa']


admin.site.register(Unidade, UnidadeAdmin)
admin.site.register(Lista, ListaAdmin)
admin.site.register(Tipo, TipoAdmin)
admin.site.register(Produto, ProdutoAdmin)
