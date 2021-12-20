from django.views.generic import ListView

from lojas.models import Loja, Departamento


class Departamentos(ListView):
    ordering = 'nome'
    template_name = 'lojas/departamentos.html'

    def get_queryset(self):
        slug = self.kwargs['slug']
        return Departamento.objects.filter(loja__slug=slug)


class Lojas(ListView):
    template_name = 'lojas/lojas.html'
    queryset = Loja.objects.filter(ativo=True)


class ContagemOpcoes(ListView):
    ordering = 'nome'
    template_name = 'lojas/opcoes.html'
    queryset = Loja.objects.filter(ativo=True)
