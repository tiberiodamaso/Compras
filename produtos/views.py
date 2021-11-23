# Create your views here.
from django.views.generic import ListView

from produtos.models import Produto


class ProdutoListView(ListView):
    ordering = 'nome'
    template_name = 'produtos/list.html'
    queryset = Produto.objects.all()
