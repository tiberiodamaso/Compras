from django.core.management.base import BaseCommand
from django.utils import timezone

from lojas.models import Departamento, Loja, Area
from produtos.models import Produto, Lista, Unidade, Tipo

UNIDADES = ['BARRA', 'BARRA 1 KG', 'BARRA 3 KG', 'BARRA 4 KG', 'BARRA 7 KG', 'CX', 'CX 8', 'CX 10', 'CX 10KG', 'CX 12', 'CX 12KG', 'CX 12 UND', 'CX 12,5', 'CX 14KG',
'CX 15', 'CX 15KG', 'CX 16', 'CX 20', 'CX 20KG', 'CX 200', 'CX 200 UND', 'CX 2000', 'CX 24', 'CX 24 UND', 'CX 25', 'CX 25 UND', 'CX 250 UND', 'CX 27', 'CX 27 UND',
'CX 30', 'CX 320 UND', 'CX 40', 'CX 40 UND', 'CX 400 UND', 'CX 48', 'CX 5 KG', 'CX 500', 'CX 500 UND', 'CX 5000', 'CX 515 KG', 'CX 6', 'CX 700 UND', 'CX 8', 'CX 25',
'FD 10', 'FD 10 OU 30', 'FD 12', 'FD 24', 'FD 30', 'FD 30 OU 10', 'FD 6', 'FD 60', 'KG', 'MILHEIRO', 'PCT', 'PCT 10', 'PCT 100', 'PCT 1000', 'PCT 60', 'RI 20', 
'ROLO', 'TI 30', 'UND', 'UND 7 KG'] 

TIPOS = ['ATACADO', 'BEBIDAS', 'DIVERSOS', 'EMBALAGEM', 'IN NATURA', 'POLPAS', 'PRODUÇÃO', 'VINHOS', 'AÇOUGUE']
LOJAS = ['MARISTA', 'PASSEIO', 'FÁBRICA']
LISTAS = ['MARISTA', 'PASSEIO']
DEPARTAMENTOS = ['BAR', 'COZINHA', 'DEMAIS', 'DEPÓSITO']
AREAS = ['BEBIDAS', 'CÂMARA CONGELADA', 'CÂMARA RESFRIADA', 'POLPAS', 'SECOS', 'VINHOS', 'IN NATURA']

class Command(BaseCommand):

    def _cleaner(self):
        print("Preparando para deleter todas as tabelas do banco de dados!")
        unidade_db = Unidade.objects.all()
        unidade_db.delete()
        tipo_db = Tipo.objects.all()
        tipo_db.delete()
        lista_db = Lista.objects.all()
        lista_db.delete()
        produto_db = Produto.objects.all()
        produto_db.delete()
        loja_db = Loja.objects.all()
        loja_db.delete()
        departamento_db = Departamento.objects.all()
        departamento_db.delete()
        area_db = Area.objects.all()
        area_db.delete()
        print("Banco de dados deletado.")

    def _criar_unidades(self):
        print("Populando a tabela Unidades")
        for i, unidade in enumerate(UNIDADES):
            unidade_db = Unidade(i + 1, unidade)
            unidade_db.save()

    def _criar_tipos(self):
        print("Populando a tabela Tipos")
        for i, tipo in enumerate(TIPOS):
            tipo_db = Tipo(i + 1, tipo)
            tipo_db.save()

    def _criar_lojas(self):
        print("Populando a tabela Lojas")
        for i, loja in enumerate(LOJAS):
            loja_db = Loja(i + 1, loja)
            loja_db.save()

    def _criar_listas(self):
        print("Populando a tabela Listas")
        for i, lista in enumerate(LISTAS):
            lista_db = Lista(i + 1, lista)
            lista_db.created = timezone.now()
            lista_db.save()

    def _criar_departamentos(self):
        print("Populando a tabela Departamentos")
        loja = Loja.objects.filter(id=1)[0]
        for i, departamento in enumerate(DEPARTAMENTOS):
            departamento_db = Departamento(i + 1, departamento)
            departamento_db.loja = loja
            departamento_db.save()

    def _criar_areas(self):
        print("Populando a tabela Áreas")
        departamento = Departamento.objects.filter(id=1)[0]
        for i, area in enumerate(AREAS):
            area_db = Area(i + 1, area)
            area_db.departamento = departamento
            area_db.cor = '#f5dbcb'
            area_db.save()

    def _criar_produtos(self):
        print("Populando a tabela Produtos")
        nome = 'Açafrão'
        tipo = Tipo.objects.filter(id=1)[0]
        unidade = Unidade.objects.filter(id=1)[0]
        descricao = 'Uma descrição inicial'
        loja = Loja.objects.filter(id=1)[0]
        lista = Lista.objects.filter(id=1)[0]
        departamento = Departamento.objects.filter(id=1)[0]
        area = Area.objects.filter(id=1)[0]
        created = timezone.now()
        qtd = 0
        media = 10

        produto_db = Produto(nome=nome, tipo=tipo, lista=lista, unidade=unidade, descricao=descricao, loja=loja,
                             departamento=departamento, area=area, qtd=qtd, media=media, created=created)
        produto_db.save()

    # def _criar_superuser(self):
    #     username = "tiberio"
    #     print(f"Criando superuser: {username}")
    #     first_name = "Tibério"
    #     last_name = 'Mendonça'
    #     password = make_password("123")
    #     is_staff = True
    #     is_active = True
    #     is_superuser = True
    #     user_account = User(username=username,
    #                         is_staff=is_staff,
    #                         is_active=is_active,
    #                         is_superuser=is_superuser,
    #                         first_name=first_name,
    #                         last_name=last_name,
    #                         password=password)
    #     user_account.save()

    def handle(self, *args, **options):

        if input('\nDeseja popular as tabelas do banco de dados? (y/n): ') == str.lower("y"):
            self._criar_tipos()
            self._criar_unidades()
            self._criar_lojas()
            self._criar_departamentos()
            self._criar_listas()
            self._criar_areas()
            # self._criar_produtos()
            # self._criar_superuser()
            print("\nBanco populado com sucesso!!")
        else:
            print("\nFalha ao popular o banco de dados..")
