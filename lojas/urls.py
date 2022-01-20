from django.urls import path

from lojas.views import Lojas, Departamentos, ListaDeComprasOpcoes, Imprimir
from produtos.views import produtos, ListaDeComprasPorLoja, ListaDeComprasTotal

app_name = 'lojas'

urlpatterns = [
    path('', Lojas.as_view(), name='lojas'),
    path('<slug:slug>/departamentos/', Departamentos.as_view(), name='departamentos'),
    path('<slug:slug>/departamentos/<str:nome>/', produtos, name='produtos'),
    path('lista-de-compras/', ListaDeComprasOpcoes.as_view(), name='lista_de_compras_opcoes'),
    path('lista-de-compras/<slug:slug>/', ListaDeComprasPorLoja.as_view(), name='lista_de_compras_por_loja'),
    path('lista-de-compras-total/', ListaDeComprasTotal.as_view(), name='lista_de_compras_total'),
    path('imprimir/lista-de-compras/<slug:slug>/', Imprimir.as_view(), name='imprimir'),

]
