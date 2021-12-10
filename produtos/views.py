# Create your views here.
from django.views.generic import ListView

from produtos.forms import ProdutoForm
from produtos.models import Produto


class ProdutoList(ListView):
    ordering = 'nome'
    template_name = 'produtos/produtos.html'
    queryset = Produto.objects.all()


class Produtos(ListView):
    ordering = 'nome'
    template_name = 'produtos/produtos.html'

    def get_context_data(self, **kwargs):
        context = super(Produtos, self).get_context_data(**kwargs)
        context['form'] = ProdutoForm()
        context['departamento'] = self.kwargs['nome'].capitalize()
        return context

    def get_queryset(self):
        slug = self.kwargs['slug']
        nome = self.kwargs['nome'].upper()
        return Produto.objects.filter(departamento__loja__slug=slug, departamento__nome=nome)


class Contagem(ListView):
    ordering = 'nome'
    template_name = 'produtos/contagem.html'

    def get_context_data(self, **kwargs):
        context = super(Contagem, self).get_context_data(**kwargs)
        context['slug'] = self.kwargs['slug'].capitalize()
        return context

    def get_queryset(self):
        slug = self.kwargs['slug']
        return Produto.objects.filter(departamento__loja__slug=slug)
