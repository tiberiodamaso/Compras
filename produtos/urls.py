from django.urls import path

from produtos.views import ProdutoList

app_name = 'produtos'

urlpatterns = [
    path('', ProdutoList.as_view(), name='list'),
]
