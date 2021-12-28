from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from lojas.models import Departamento, Loja
from produtos.models import Produto, Lista, Unidade

UNIDADES = ['KG', 'SC', 'FD', 'UN', 'ML', 'L']
LISTAS = ['ATACADISTA', 'BEBIDAS', 'EMBALAGENS', 'DIVERSOS', 'POLPAS', 'IN NATURA', 'CARNES PRODUZIR',
          'COZINHA PRODUZIR']
LOJAS = ['MARISTA', 'PASSEIO', 'FÁBRICA']
DEPARTAMENTOS = ['COZINHA', 'BAR', 'POLPAS', 'FÁBRICA']


class Command(BaseCommand):

    def _cleaner(self):
        print("Preparando para deleter todas as tabelas do banco de dados!")
        produto_db = Produto.objects.all()
        produto_db.delete()
        loja_db = Loja.objects.all()
        loja_db.delete()
        departamento_db = Departamento.objects.all()
        departamento_db.delete()
        print("Banco de dados deletado.")

    def _criar_unidades(self):
        print("Populando a tabela Unidades")
        for i, unidade in enumerate(UNIDADES):
            unidade_db = Unidade(i + 1, unidade)
            unidade_db.save()

    def _criar_listas(self):
        print("Populando a tabela Listas")
        for i, lista in enumerate(LISTAS):
            lista_db = Lista(i + 1, lista)
            lista_db.save()

    def _criar_lojas(self):
        print("Populando a tabela Lojas")
        for i, loja in enumerate(LOJAS):
            loja_db = Loja(i + 1, loja)
            loja_db.save()

    def _criar_departamentos(self):
        print("Populando a tabela Departamentos")
        loja = Loja.objects.filter(id=1)[0]
        for i, departamento in enumerate(DEPARTAMENTOS):
            departamento_db = Departamento(i + 1, departamento)
            departamento_db.loja = loja
            departamento_db.save()

    def _criar_produtos(self):
        print("Populando a tabela Produtos")
        nome = 'Açafrão'
        lista = Lista.objects.filter(id=1)[0]
        unidade = Unidade.objects.filter(id=1)[0]
        descricao = 'Uma descrição inicial'
        departamento = Departamento.objects.filter(id=1)[0]
        loja = Loja.objects.filter(id=1)[0]
        qtd = 5

        produto_db = Produto(nome=nome, lista=lista, unidade=unidade, descricao=descricao, departamento=departamento,
                             loja=loja, qtd=qtd)
        produto_db.save()

    def _criar_superuser(self):
        username = "tiberio"
        print(f"Criando superuser: {username}")
        first_name = "Tibério"
        last_name = 'Mendonça'
        password = make_password("123")
        is_staff = True
        is_active = True
        is_superuser = True
        user_account = User(username=username,
                            is_staff=is_staff,
                            is_active=is_active,
                            is_superuser=is_superuser,
                            first_name=first_name,
                            last_name=last_name,
                            password=password)
        user_account.save()

    def handle(self, *args, **options):

        if input('\nDeseja popular as tabelas do banco de dados? (y/n): ') == str.lower("y"):
            self._criar_unidades()
            self._criar_listas()
            self._criar_lojas()
            self._criar_departamentos()
            self._criar_produtos()
            self._criar_superuser()
            print("\nBanco populado com sucesso!!")
        else:
            print("\nFalha ao popular o banco de dados..")
