from django.urls import path

from lojas.views import Lojas, Departamentos, ContagemOpcoes, Imprimir
from produtos.views import produtos, ContagemPorLoja, ContagemGeral

app_name = 'lojas'

urlpatterns = [
    path('', Lojas.as_view(), name='lojas'),
    path('<slug:slug>/departamentos/', Departamentos.as_view(), name='departamentos'),
    path('<slug:slug>/departamentos/<str:nome>/', produtos, name='produtos'),
    path('contagem/', ContagemOpcoes.as_view(), name='contagem_opcoes'),
    path('contagem/<slug:slug>/', ContagemPorLoja.as_view(), name='contagem'),
    path('contagem-geral/', ContagemGeral.as_view(), name='contagem_geral'),
    path('imprimir/contagem/<slug:slug>/', Imprimir.as_view(), name='imprimir'),

]
