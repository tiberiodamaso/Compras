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


class Lojas(ListView):
    template_name = 'lojas/lojas.html'
    queryset = Loja.objects.filter(ativo=True)


class ContagemOpcoes(ListView):
    ordering = 'nome'
    template_name = 'lojas/opcoes.html'
    queryset = Loja.objects.filter(ativo=True)


class Imprimir(PDFView):
    """
    A PDFView behaves pretty much like a TemplateView, so you can treat it as such.
    """
    template_name = 'produtos/contagem-pdf.html'
    prompt_download = True
    download_name = 'Teste.pdf'

    def get_context_data(self, *args, **kwargs):
        """Pass some extra context to the template."""
        context = super().get_context_data(*args, **kwargs)
        slug = self.kwargs['slug']
        context['loja'] = slug
        context['produtos'] = Produto.objects.filter(loja__slug=slug)

        return context
