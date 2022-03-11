import datetime

from django.db.models import Sum
from django.views.generic import ListView
from django_renderpdf.views import PDFView
from guardian.shortcuts import get_objects_for_user

from lojas.models import Loja, Departamento
from produtos.models import Produto, Contagem


# class Departamentos(ListView):
    # ordering = 'nome'
    # template_name = 'lojas/departamentos.html'

    # def get_queryset(self):
    #     slug = self.kwargs['slug']
    #     return Departamento.objects.filter(loja__slug=slug)

    # def get_context_data(self, *args, **kwargs):
        # context = super().get_context_data(*args, **kwargs)
        # slug = self.kwargs['slug']
        # context['loja'] = Loja.objects.get(slug=slug).nome
        # context['slug'] = slug
        # return context

class Departamentos(ListView):
    ordering = 'nome'
    template_name = 'lojas/departamentos.html'

    def get_queryset(self):
        user = self.request.user
        departamentos = Departamento.objects.all()
        queryset = get_objects_for_user(user, ['cozinha marista', 'cozinha passeio'], klass=departamentos, any_perm=True)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        slug = self.kwargs['slug']
        context['loja'] = Loja.objects.get(slug=slug).nome
        context['slug'] = slug
        return context


# class Lojas(ListView):
    # ordering = 'nome'
    # template_name = 'lojas/lojas.html'
    # queryset = Loja.objects.filter(ativo=True)


class Lojas(ListView):
    template_name = 'lojas/lojas.html'

    def get_queryset(self):
        user = self.request.user
        lojas = Loja.objects.all()
        queryset = get_objects_for_user(user, ['marista', 'passeio', 'fabrica'], klass=lojas, any_perm=True)
        return queryset


class ListaDeComprasOpcoes(ListView):
    ordering = 'nome'
    template_name = 'lojas/lojas-opcoes.html'
    queryset = Loja.objects.filter(ativo=True).exclude(slug='fabrica')

    # def get_context_data(self, **kwargs):
    #     context = super(ListaDeComprasOpcoes, self).get_context_data(**kwargs)
    #     lista = self.kwargs['lista-de-compras']
    #     context['lista'] = lista
    #     return context


class Imprimir(PDFView):
    """
    A PDFView behaves pretty much like a TemplateView, so you can treat it as such.
    """
    def get_context_data(self, *args, **kwargs):
        """Pass some extra context to the template."""
        context = super().get_context_data(*args, **kwargs)
        slug = self.kwargs['slug']
        # comprar = self.request.GET.getlist('comprar')
        produtos = []
        for obj in self.request.GET.lists():
            if 'on' in obj[1]:
                produto = Produto.objects.get(id=int(obj[0]))
                produto.comprar = obj[1][2]
                produtos.append(produto)
        if slug == 'total':
            context['loja'] = 'TOTAL'
            context['produtos'] = Produto.objects.all().values('nome', 'lista__nome').annotate(qtd=Sum('qtd'))
        else:
            context['loja'] = Loja.objects.get(slug=slug).nome
            # context['produtos'] = Produto.objects.filter(loja__slug=slug).order_by('tipo__nome', 'nome')
            context['produtos'] = produtos
            context['data'] = datetime.datetime.now()

        return context

    def get_download_name(self, **kwargs) -> str:
        context = super().get_context_data(**kwargs)
        slug = self.kwargs['slug']
        return f'lista-de-compras-{slug}.pdf'

    template_name = 'produtos/lista-de-compras-por-loja-pdf.html'
    prompt_download = True
    download_name = get_download_name


class ImprimirContagem(PDFView):
    """
    A PDFView behaves pretty much like a TemplateView, so you can treat it as such.
    """
    def get_context_data(self, *args, **kwargs):
        """Pass some extra context to the template."""
        context = super().get_context_data(*args, **kwargs)
        contagem = Contagem.objects.get(id=self.kwargs['pk'])
        context['contagem'] = contagem
        return context

    def get_download_name(self, **kwargs) -> str:
        context = super().get_context_data(**kwargs)
        contagem = Contagem.objects.get(id=self.kwargs['pk'])
        context['nome'] = contagem.nome
        context['data'] = contagem.data
        return f'contagem-{contagem.nome.lower()}-{contagem.data.strftime("%d-%m-%Y - %Hh%Mmin")}.pdf'

    template_name = 'produtos/contagem-por-loja-pdf.html'
    prompt_download = True
    download_name = get_download_name
