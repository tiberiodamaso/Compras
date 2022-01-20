from django.db.models import Sum
from django.views.generic import ListView
from django_renderpdf.views import PDFView

from lojas.models import Loja, Departamento
from produtos.models import Produto


class Departamentos(ListView):
    ordering = 'nome'
    template_name = 'lojas/departamentos.html'

    def get_queryset(self):
        slug = self.kwargs['slug']
        return Departamento.objects.filter(loja__slug=slug)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        slug = self.kwargs['slug']
        context['loja'] = Loja.objects.get(slug=slug).nome
        return context


class Lojas(ListView):
    ordering = 'nome'
    template_name = 'lojas/lojas.html'
    queryset = Loja.objects.filter(ativo=True)


class ListaDeComprasOpcoes(ListView):
    ordering = 'nome'
    template_name = 'lojas/lojas-opcoes.html'
    queryset = Loja.objects.filter(ativo=True).exclude(slug='fabrica')


class Imprimir(PDFView):
    """
    A PDFView behaves pretty much like a TemplateView, so you can treat it as such.
    """
    def get_context_data(self, *args, **kwargs):
        """Pass some extra context to the template."""
        context = super().get_context_data(*args, **kwargs)
        slug = self.kwargs['slug']
        if slug == 'total':
            context['loja'] = 'TOTAL'
            context['produtos'] = Produto.objects.all().values('nome', 'lista__nome').annotate(qtd=Sum('qtd'))
        else:
            context['loja'] = Loja.objects.get(slug=slug).nome
            context['produtos'] = Produto.objects.filter(loja__slug=slug).order_by('tipo__nome', 'nome')

        return context

    def get_download_name(self, **kwargs) -> str:
        context = super().get_context_data(**kwargs)
        slug = self.kwargs['slug']
        return f'lista-de-compras-{slug}.pdf'

    template_name = 'produtos/lista-de-compras-por-loja-pdf.html'
    prompt_download = True
    download_name = get_download_name
