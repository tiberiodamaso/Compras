from django.urls import path

from produtos.views import cadastra_produtos_planilha

app_name = 'produtos'

urlpatterns = [
    path('planilha/', cadastra_produtos_planilha, name='planilha')
]
