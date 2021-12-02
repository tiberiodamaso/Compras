from django.urls import path

from lojas.views import LojaList, DepartamentoList
from produtos.views import DepartamentoProdutoList

app_name = 'lojas'

urlpatterns = [
    path('', LojaList.as_view(), name='lojas_list'),
    path('<slug:slug>/departamentos/', DepartamentoList.as_view(), name='departamentos_list'),
    path('<slug:slug>/departamentos/<str:nome>/', DepartamentoProdutoList.as_view(), name='produtos_list'),
]
