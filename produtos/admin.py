from django.contrib import admin

from produtos.models import Produto, Unidade, Lista, Tipo, Contagem


# Register your models here.


class UnidadeAdmin(admin.ModelAdmin):
    list_display = ['nome', 'ativo']
    list_filter = ['nome', 'ativo']
    search_fields = ['nome']


class TipoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'ativo']
    list_filter = ['nome', 'ativo']
    search_fields = ['nome']


class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['tipo', 'nome', 'loja', 'departamento', 'area', 'qtd', 'media', 'comprar', 'contagem']
    list_filter = ['tipo', 'loja', 'departamento', 'area']
    search_fields = ['nome']
    readonly_fields = ['pesquisa']
    list_display_links =['nome']


# class ProdutoInline(admin.TabularInline):
#     model = Produto


class ListaAdmin(admin.ModelAdmin):
    # list_display = ['nome', 'get_qtd', 'get_comprar',  'created', 'ativo']
    list_display = ['nome', 'created', 'ativo', 'id']
    list_filter = ['nome', 'ativo']
    search_fields = ['nome']
    # inlines = [ProdutoInline]

    # @display(description='produto')
    # def get_produto(self, obj):
    #     return obj.produto
    #
    # @display(description='qtd')
    # def get_qtd(self, obj):
    #     return obj.produto.qtd
    #
    # @display(description='comprar')
    # def get_comprar(self, obj):
    #     return obj.produto.comprar


class ContagemAdmin(admin.ModelAdmin):
    list_display = ['nome', 'data', 'id']
    list_filter = ['nome', 'data']


admin.site.register(Unidade, UnidadeAdmin)
admin.site.register(Lista, ListaAdmin)
admin.site.register(Tipo, TipoAdmin)
admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Contagem, ContagemAdmin)
