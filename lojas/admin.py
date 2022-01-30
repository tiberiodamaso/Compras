from django.contrib import admin

from lojas.models import Departamento, Loja, Area


class LojaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'slug', 'ativo']


class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'loja', 'slug', 'ativo']
    list_filter = ['loja', 'nome']


class AreaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'slug',  'departamento', 'cor', 'ativo']
    list_filter = ['departamento', 'nome']


admin.site.register(Loja, LojaAdmin)
admin.site.register(Departamento, DepartamentoAdmin)
admin.site.register(Area, AreaAdmin)
admin.site.site_header = 'Caseratto'
admin.site.site_title = 'Caseratto'
admin.site.index_title = 'Administração do Compras'
