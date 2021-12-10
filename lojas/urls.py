from django.urls import path

from lojas.views import Lojas, Departamentos, LojasContagem
from produtos.views import Produtos, Contagem

app_name = 'lojas'

urlpatterns = [
    path('', Lojas.as_view(), name='lojas'),
    path('<slug:slug>/departamentos/', Departamentos.as_view(), name='departamentos'),
    path('<slug:slug>/departamentos/<str:nome>/', Produtos.as_view(), name='produtos'),
    path('contagem/', LojasContagem.as_view(), name='contagem'),
    path('contagem/<slug:slug>/', Contagem.as_view(), name='contagem_loja'),

]
