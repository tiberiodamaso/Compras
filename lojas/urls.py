from django.urls import path

from lojas.views import Departamentos, Departamentos2, ListaDeComprasOpcoes, Imprimir, ImprimirContagem, Lojas2
from produtos.views import finalizar_contagem, zerar_contagem, ListaDeComprasTotal, TiposDeProdutos, \
    ComprasPorTipo, ContagensRealizadas, ContagemDetalhe

app_name = 'lojas'

urlpatterns = [

    # LOJAS
    path('', Lojas2.as_view(), name='lojas'),
    path('<slug:slug>/departamentos/', Departamentos2.as_view(), name='departamentos'),
    path('<slug:slug>/departamentos/<str:nome>/', finalizar_contagem, name='contagem'),

    # LISTA DE COMPRAS
    path('compras/', ListaDeComprasOpcoes.as_view(), name='lista_de_compras_opcoes'),
    # path('compras/<slug:slug>/', ListaDeComprasPorLoja.as_view(), name='lista_de_compras_por_loja'),
    path('compras/<slug:slug>/opcoes/', TiposDeProdutos.as_view(), name='tipos_de_produtos'),
    path('compras/<slug:slug>/<str:nome>/', ComprasPorTipo.as_view(), name='compras_por_tipo'),
    path('compras-total/', ListaDeComprasTotal.as_view(), name='lista_de_compras_total'),

    # IMPRIMIR
    path('imprimir/compras/<slug:slug>/', Imprimir.as_view(), name='imprimir'),
    path('imprimir/contagem/<int:pk>/', ImprimirContagem.as_view(), name='imprimir_contagem'),

    # CONTAGEM
    path('contagem/<slug:slug>/zerar-contagem/', zerar_contagem, name='zerar_contagem'),
    path('contagem/realizadas/<slug:slug>', ContagensRealizadas.as_view(), name='contagens_realizadas'),
    path('contagem/<int:pk>/', ContagemDetalhe.as_view(), name='contagem_detalhe'),

]
