# Create your views here.
from django.views.generic import ListView

from produtos.models import Produto


class ProdutoList(ListView):
    ordering = 'nome'
    template_name = 'produtos/produtos.html'
    queryset = Produto.objects.all()


class DepartamentoProdutoList(ListView):
    ordering = 'nome'
    template_name = 'produtos/produtos.html'

    def get_queryset(self):
        slug = self.kwargs['slug']
        nome = self.kwargs['nome'].upper()
        return Produto.objects.filter(departamento__loja__slug=slug, departamento__nome=nome)
