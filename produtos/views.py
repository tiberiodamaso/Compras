# Create your views here.
from django.contrib import messages
from django.db.models import Count, Sum
from django.shortcuts import render
from django.views.generic import ListView

from lojas.models import Loja, Departamento
from produtos.forms import ProdutoForm
from produtos.models import Produto


class Contagem(ListView):
    ordering = 'nome'
    context_object_name = 'produtos'

    def get_template_names(self):
        return ['produtos/contagem.html']

    def get_queryset(self):
        slug = self.kwargs['slug']
        if slug != 'geral':
            template_name = 'produtos/contagem.html'
            return Produto.objects.filter(loja__slug=slug)
        else:
            template_name = 'produtos/contagem.html'
            return Produto.objects.all().values('nome', 'lista__nome', 'unidade__nome').annotate(total=Sum('qtd'))

    def get_context_data(self, **kwargs):
        context = super(Contagem, self).get_context_data(**kwargs)
        context['loja'] = self.kwargs['slug'].capitalize()
        return context


class ContagemGeral(ListView):
    template_name = 'produtos/contagem-geral.html'
    context_object_name = 'produtos'

    def get_queryset(self):
        return Produto.objects.all().values('nome').annotate(total=Count('nome'))


def produtos(request, slug, nome):
    form = ProdutoForm()
    loja = Loja.objects.get(slug=slug)
    departamento = Departamento.objects.get(nome=nome.upper(), loja=loja)
    produtos = Produto.objects.filter(departamento__nome=nome.upper(), loja__slug=slug)
    context = {'form': form, 'produtos': produtos, 'loja': loja, 'departamento': departamento}

    if request.method == 'POST':
        data = request.POST
        for index, produto_id in enumerate(data.getlist('id')):
            produto = Produto.objects.get(id=produto_id)
            produto.qtd = data.getlist('qtd')[index]
            produto.save()
        messages.success(request, 'Contagem salva com sucesso!')
        return render(request, 'produtos/confirmacao.html', context)

    return render(request, 'produtos/produtos.html', context)


# class Produtos(ListView):
#     ordering = 'nome'
#     template_name = 'produtos/produtos.html'
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
#     template_name = 'produtos/produtos.html'
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
#         # return render(request, 'produtos/produtos.html', {'object_list': queryset})
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
#         return render(request, 'produtos/confirmacao.html')
#
#     return render(request, 'produtos/produtos.html')
