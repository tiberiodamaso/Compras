from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from guardian.shortcuts import assign_perm

from lojas.models import Loja


class Command(BaseCommand):

    def _assign_marista_permission(self):
        marista = Group.objects.get(name='Marista')
        loja = Loja.objects.get(slug='marista')
        assign_perm('marista', marista, loja)

    def _assign_passeio_permission(self):
        passeio = Group.objects.get(name='Passeio')
        loja = Loja.objects.get(slug='passeio')
        assign_perm('passeio', passeio, loja)

    def _assign_fabrica_permission(self):
        fabrica = Group.objects.get(name='Fábrica')
        loja = Loja.objects.get(slug='fabrica')
        assign_perm('fabrica', fabrica, loja)

    def handle(self, *args, **options):
        self._assign_marista_permission()
        self._assign_passeio_permission()
        self._assign_fabrica_permission()
