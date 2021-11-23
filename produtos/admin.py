from django.contrib import admin

# Register your models here.
from produtos.models import Produto


class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'fornecedor', 'unidade']
    list_filter = ['nome', 'fornecedor', 'unidade']
    search_fields = ['nome', 'fornecedor']


admin.site.register(Produto, ProdutoAdmin)
