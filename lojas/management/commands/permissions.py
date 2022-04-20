from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from guardian.shortcuts import assign_perm

from lojas.models import Loja, Departamento


class Command(BaseCommand):

    def _assign_marista_permission(self):
        Group.objects.create(name='Marista')
        marista = Group.objects.get(name='Marista')
        loja = Loja.objects.get(slug='marista')
        assign_perm('marista', marista, loja)

    def _assign_passeio_permission(self):
        Group.objects.create(name='Passeio')
        passeio = Group.objects.get(name='Passeio')
        loja = Loja.objects.get(slug='passeio')
        assign_perm('passeio', passeio, loja)

    def _assign_fabrica_permission(self):
        Group.objects.create(name='Fábrica')
        fabrica = Group.objects.get(name='Fábrica')
        loja = Loja.objects.get(slug='fabrica')
        assign_perm('fabrica', fabrica, loja)

    def _assign_cozinha_marista_permission(self):
        Group.objects.create(name='Cozinha Marista')
        cozinha_marista = Group.objects.get(name='Cozinha Marista')
        departamento = Departamento.objects.get(slug='cozinha', loja__slug='marista')
        assign_perm('cozinha marista', cozinha_marista, departamento)

    def _assign_cozinha_passeio_permission(self):
        Group.objects.create(name='Cozinha Passeio')
        cozinha_passeio = Group.objects.get(name='Cozinha Passeio')
        departamento = Departamento.objects.get(slug='cozinha', loja__slug='passeio')
        assign_perm('cozinha passeio', cozinha_passeio, departamento)

    def handle(self, *args, **options):
        self._assign_marista_permission()
        self._assign_passeio_permission()
        self._assign_fabrica_permission()
        self._assign_cozinha_marista_permission()
        self._assign_cozinha_passeio_permission()
