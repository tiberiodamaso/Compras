from django.contrib import admin
# Register your models here.
from django.contrib.admin import display

from produtos.models import Produto, Unidade, Lista, Tipo, Contagem


class UnidadeAdmin(admin.ModelAdmin):
    list_display = ['nome', 'ativo']
    list_filter = ['nome', 'ativo']
    search_fields = ['nome']


class ListaAdmin(admin.ModelAdmin):
    # list_display = ['nome', 'get_qtd', 'get_comprar',  'created', 'ativo']
    list_display = ['nome', 'created', 'ativo', 'id']
    list_filter = ['nome', 'ativo']
    search_fields = ['nome']

    # @display(description='qtd')
    # def get_qtd(self, obj):
    #     return obj.contagem.qtd
    #
    # @display(description='comprar')
    # def get_comprar(self, obj):
    #     return obj.contagem.comprar


class TipoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'ativo']
    list_filter = ['nome', 'ativo']
    search_fields = ['nome']


class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'loja', 'departamento', 'area', 'tipo', 'media', 'id']
    list_filter = ['nome', 'loja', 'departamento']
    search_fields = ['nome']
    readonly_fields = ['pesquisa']


class ContagemAdmin(admin.ModelAdmin):
    list_display = ['produto', 'get_loja', 'qtd', 'comprar', 'created']
    list_filter = ['produto']
    readonly_fields = ['comprar']

    @display(description='Loja')
    def get_loja(self, obj):
        return obj.produto.loja


admin.site.register(Unidade, UnidadeAdmin)
admin.site.register(Lista, ListaAdmin)
admin.site.register(Tipo, TipoAdmin)
admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Contagem, ContagemAdmin)
