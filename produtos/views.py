import datetime

from django.contrib import messages
from django.db.models import Sum
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from lojas.models import Loja, Departamento
from produtos.models import Produto, Lista, Tipo, Contagem


class ListaDeComprasPorLoja(ListView):
    ordering = 'nome'
    context_object_name = 'produtos'
    template_name = 'produtos/lista-de-compras-por-loja.html'

    def get_queryset(self):
        slug = self.kwargs['slug']
        lista = Lista.objects.filter(nome=slug.upper()).order_by('created').first()
        # return lista.contagem.all().order_by('produto__tipo__nome', 'produto').exclude(comprar=0)
        return lista.produtos.all().exclude(comprar=0).order_by('tipo', 'nome')
        # return Produto.objects.filter(loja__slug=slug)

    def get_context_data(self, **kwargs):
        context = super(ListaDeComprasPorLoja, self).get_context_data(**kwargs)
        context['loja'] = Loja.objects.get(slug=self.kwargs['slug']).nome
        context['slug'] = self.kwargs['slug']
        return context


class TiposDeProdutos(ListView):
    ordering = 'nome'
    context_object_name = 'tipos'
    template_name = 'produtos/tipos-de-produtos.html'

    def get_queryset(self):
        return Tipo.objects.all().order_by('nome')

    def get_context_data(self, **kwargs):
        context = super(TiposDeProdutos, self).get_context_data(**kwargs)
        # context['loja'] = Loja.objects.get(slug=self.kwargs['slug']).nome
        context['slug'] = self.kwargs['slug']
        return context


class ComprasPorTipo(ListView):
    ordering = 'nome'
    context_object_name = 'produtos'
    template_name = 'produtos/compras-por-tipo.html'

    def get_queryset(self):
        slug = self.kwargs['slug']
        tipo = self.kwargs['nome']
        lista = Lista.objects.filter(nome=slug.upper()).order_by('created').first()
        return lista.produtos.filter(tipo__nome=tipo.upper()).exclude(comprar=0).order_by('nome')

    def get_context_data(self, **kwargs):
        context = super(ComprasPorTipo, self).get_context_data(**kwargs)
        context['loja'] = Loja.objects.get(slug=self.kwargs['slug']).nome
        context['slug'] = self.kwargs['slug']
        context['tipo'] = self.kwargs['nome']
        return context


class ListaDeComprasTotal(ListView):
    ordering = 'nome'
    template_name = 'produtos/lista-de-compras-total.html'
    context_object_name = 'produtos'

    def get_queryset(self):
        return Produto.objects.all().values('nome', 'lista__nome', 'unidade__nome').annotate(total=Sum('qtd'))

    def get_context_data(self, **kwargs):
        context = super(ListaDeComprasTotal, self).get_context_data(**kwargs)
        context['slug'] = 'total'
        return context


def contagem(request, slug, nome):
    loja = Loja.objects.get(slug=slug)
    departamento = Departamento.objects.get(nome=nome.upper(), loja=loja)
    produtos = Produto.objects.filter(departamento__nome=nome.upper(), loja__slug=slug).order_by('area', 'nome')
    context = {'produtos': produtos, 'loja': loja, 'departamento': departamento}

    if request.method == 'POST':
        data = request.POST
        # try:
        #     lista = Lista.objects.get(nome=loja)
        # except:
        #     lista = Lista.objects.create(nome=loja)
        # lista = Lista.objects.get_or_create(nome=loja)
        for index, produto_id in enumerate(data.getlist('id')):
            produto = Produto.objects.get(id=produto_id)
            # contagem = Contagem.objects.create(produto=produto, qtd=int(data.getlist('qtd')[index]))
            # lista.contagem.add(contagem)
            # lista.save()
            # contagem.produto = produto
            # contagem.qtd = data.getlist('qtd')[index]
            produto.qtd = int(data.getlist('qtd')[index])
            produto.save()
            # contagem.save()

        messages.success(request, 'Contagem finalizada!')
        return render(request, 'produtos/confirmacao-contagem.html', context)

    return render(request, 'produtos/contagem.html', context)


def zerar_contagem(request, slug):
    loja = Loja.objects.get(slug=slug)
    produtos = Produto.objects.filter(loja__slug=slug)
    context = {'produtos': produtos, 'loja': loja}
    contagem = Contagem.objects.create(nome=loja.nome, data=datetime.datetime.now())
    for produto in produtos:
        contagem.produtos.add(produto)
        produto.qtd = 0
        produto.save()
    messages.success(request, f'Contagem {slug} zerada!')
    return render(request, 'produtos/confirmacao-contagem-zerada.html', context)


class Contagens(ListView):
    ordering = 'data'
    template_name = 'produtos/contagens.html'
    context_object_name = 'contagens'

    def get_queryset(self):
        return Contagem.objects.all().order_by('nome', '-data')


class ContagemDetalhe(DetailView):
    model = Contagem
    template_name = 'produtos/contagem-detalhe.html'
    context_object_name = 'contagem'




# class Produtos(ListView):
#     ordering = 'nome'
#     template_name = 'produtos/contagem.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(Produtos, self).get_context_data(**kwargs)
#         context['form'] = ProdutoForm()
#         context['loja'] = self.kwargs['slug'].capitalize()
#         context['departamento'] = self.kwargs['nome'].capitalize()
#         return context
#
#     def get_queryset(self):
#         slug = self.kwargs['slug']
#         nome = self.kwargs['nome'].upper()
#         return Produto.objects.filter(departamento__loja__slug=slug, departamento__nome=nome)
#
#
# class Produtos(UpdateView):
#     ordering = 'nome'
#     template_name = 'produtos/contagem.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(Produtos, self).get_context_data(**kwargs)
#         context['form'] = ProdutoForm()
#         context['loja'] = self.kwargs['slug'].capitalize()
#         context['departamento'] = self.kwargs['nome'].capitalize()
#         return context
#
#     def get_queryset(self, *args, **kwargs):
#         slug = self.kwargs['slug']
#         nome = self.kwargs['nome'].upper()
#         queryset = Produto.objects.filter(departamento__loja__slug=slug, departamento__nome=nome)
#         return queryset
#
#     def get(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         # return render(request, 'produtos/contagem.html', {'object_list': queryset})
#         return super().get(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         data = request.POST
#         for index, produto_id in enumerate(data.getlist('id')):
#             produto = Produto.objects.get(id=produto_id)
#             produto.qtd = data.getlist('qtd')[index]
#             produto.save()
#         messages.success(request, 'Contagem salva com sucesso!')
#         return super().post(request, *args, **kwargs)


# def Contagem(request):
#     if request.method == 'POST':
#         data = request.POST
#         for index, produto_id in enumerate(data.getlist('id')):
#             produto = Produto.objects.get(id=produto_id)
#             produto.qtd = data.getlist('qtd')[index]
#             produto.save()
#         messages.success(request, 'Contagem salva com sucesso!')
#         return render(request, 'produtos/confirmacao-lista-de-compras-por-loja.html')
#
#     return render(request, 'produtos/contagem.html')
