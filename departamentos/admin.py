from django.contrib import admin

from departamentos.models import Departamento, Loja


class LojaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'ativo']


# Register your models here.
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ['loja', 'nome', 'ativo']
    list_filter = ['loja', 'nome']


admin.site.register(Loja, LojaAdmin)
admin.site.register(Departamento, DepartamentoAdmin)
admin.site.site_header = 'Caseratto'
admin.site.site_title = 'Caseratto'
admin.site.index_title = 'Administração do Compras'
