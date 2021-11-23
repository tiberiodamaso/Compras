from django.urls import path

from produtos.views import ProdutoListView

urlpatterns = [
    path('', ProdutoListView.as_view(), name='list'),
]
