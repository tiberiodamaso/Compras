import datetime

from django.contrib import messages
from django.db.models import Sum
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from lojas.models import Loja, Departamento, Area
from produtos.forms import PlanilhaForm
from produtos.models import Produto, Lista, Tipo, Contagem, Unidade
from produtos.utils import read_csv, get_unidade_por_nome, cleaner


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
        return Tipo.objects.all().order_by('nome').exclude(nome='PROCESSADOS')

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
        tipo = self.kwargs['tipo']
        lista = Lista.objects.filter(nome=slug.upper()).order_by('created').first()
        lista_por_tipo = lista.produtos.filter(tipo__nome=tipo.upper()).order_by('nome')
        lista_agrupada_por_total = lista_por_tipo.values('nome', 'unidade_contagem__nome', 'unidade_compra__nome' ).annotate(comprar=Sum('comprar'), qtd=Sum('qtd'), media=Sum('media'))
        lista_agrupada_por_total = lista_agrupada_por_total.exclude(comprar=0)
        # return lista.produtos.filter(tipo__nome=tipo.upper()).exclude(comprar=0).order_by('nome')
        return lista_agrupada_por_total

    def get_context_data(self, **kwargs):
        context = super(ComprasPorTipo, self).get_context_data(**kwargs)
        context['loja'] = Loja.objects.get(slug=self.kwargs['slug']).nome
        context['slug'] = self.kwargs['slug']
        context['tipo'] = self.kwargs['tipo']
        return context


class ListaDeComprasTotal(ListView):
    ordering = 'nome'
    template_name = 'produtos/lista-de-compras-total.html'
    context_object_name = 'produtos'

    def get_queryset(self):
        return Produto.objects.all().values('nome', 'lista__nome', 'unidade_contagem__nome').annotate(total=Sum('qtd'))

    def get_context_data(self, **kwargs):
        context = super(ListaDeComprasTotal, self).get_context_data(**kwargs)
        context['slug'] = 'total'
        return context


def finalizar_contagem(request, slug, nome):
    loja = Loja.objects.get(slug=slug)
    departamento = Departamento.objects.get(nome=nome.upper(), loja=loja)
    produtos = Produto.objects.filter(departamento__nome=nome.upper(), loja__slug=slug).order_by('numero')
    context = {'produtos': produtos, 'loja': loja, 'departamento': departamento}

    if request.method == 'POST':
        data = request.POST
        try:
            contagem = Contagem.objects.filter(nome=loja.nome).order_by('-data').first()
            if not contagem:
                contagem = Contagem.objects.create(nome=loja.nome, data=datetime.datetime.now())
        except:
            print('Um erro ocorreu')
            # contagem = Contagem.objects.create(nome=loja.nome, data=datetime.datetime.now())
        # contagem = Contagem.objects.get_or_create(nome=loja.nome, data=datetime.datetime.now())
        for index, produto_id in enumerate(data.getlist('id')):
            produto = Produto.objects.get(id=produto_id)
            contagem.produtos.add(produto)
            produto.qtd = float(data.getlist('qtd')[index])
            produto.contagem = produto.qtd
            produto.save()
            # contagem.save()

        messages.success(request, 'Contagem finalizada!')
        return render(request, 'produtos/confirmacao-contagem.html', context)

    return render(request, 'produtos/contagem.html', context)


def zerar_contagem(request, slug):
    loja = Loja.objects.get(slug=slug)
    produtos = Produto.objects.filter(loja__slug=slug)
    context = {'produtos': produtos, 'loja': loja}
    # contagem = Contagem.objects.filter(nome=loja.nome).order_by('-data').first()
    contagem = Contagem.objects.create(nome=loja.nome, data=datetime.datetime.now())
    for produto in produtos:
        # contagem.produtos.add(produto)
        # produto.contagem = produto.qtd
        produto.qtd = 0
        produto.save()
    messages.success(request, f'Contagem {slug} zerada!')
    return render(request, 'produtos/confirmacao-contagem-zerada.html', context)


class ContagensRealizadas(ListView):
    ordering = 'data'
    template_name = 'produtos/contagens-realizadas.html'
    context_object_name = 'contagens'

    def get_context_data(self, **kwargs):
        context = super(ContagensRealizadas, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']
        context['slug'] = slug
        return context

    def get_queryset(self):
        slug = self.kwargs['slug']
        return Contagem.objects.filter(nome=slug.upper()).order_by('nome', '-data')


class ContagemDetalhe(DetailView):
    model = Contagem
    template_name = 'produtos/contagem-detalhe.html'
    context_object_name = 'contagem'


def cadastra_produtos_planilha(request):
    form = PlanilhaForm()
    unidades = Unidade.objects.all()
    if request.method == 'POST':
        data = request.FILES
        produtos_a_cadastrar = read_csv(data)
        for index, produto in enumerate(produtos_a_cadastrar):
            nome = produto['PRODUTO'].upper().strip()
            numero = produto['N']
            tipo = Tipo.objects.get(nome=produto['TIPO'].strip().upper())
            loja = Loja.objects.get(nome=produto['LOJA'].strip().upper())
            departamento = Departamento.objects.get(nome=produto['DEPARTAMENTO'].strip().upper(), loja=loja)
            area = Area.objects.get(nome=produto['AREA'].strip().upper())
            unidade_contagem = Unidade.objects.get(nome=produto['UNIDADE CONTAGEM'].strip().upper())
            unidade_compra = Unidade.objects.get(nome=produto['UNIDADE COMPRA'].strip().upper())
            lista = Lista.objects.get(nome=produto['LOJA'].strip().upper())
            media = float(produto['MÉDIA DE COMPRA'].replace(',', '.'))
            requisicao = int(produto['MÉDIA DE REQUISIÇÃO'])
            Produto.objects.update_or_create(nome=nome, numero=numero, tipo=tipo, unidade_contagem=unidade_contagem,
                                             unidade_compra=unidade_compra, loja=loja, departamento=departamento,
                                             area=area, lista=lista, media=media, requisicao=requisicao)
            print()
        messages.success(request, 'Produtos cadastrados com sucesso!')
        return render(request, 'produtos/confirmacao-cadastro-produtos.html')
    return render(request, 'produtos/planilha.html', {'form': form})

