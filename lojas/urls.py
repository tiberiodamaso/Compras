from django.urls import path

from lojas.views import Lojas, Departamentos, ContagemOpcoes
from produtos.views import produtos, Contagem

app_name = 'lojas'

urlpatterns = [
    path('', Lojas.as_view(), name='lojas'),
    path('<slug:slug>/departamentos/', Departamentos.as_view(), name='departamentos'),
    path('<slug:slug>/departamentos/<str:nome>/', produtos, name='produtos'),
    path('contagem/', ContagemOpcoes.as_view(), name='contagem_opcoes'),
    path('contagem/<slug:slug>/', Contagem.as_view(), name='contagem'),

]
