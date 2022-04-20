from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

from django.urls import path, include

from lojas.views import Lojas, Departamentos, ListaDeComprasOpcoes, Imprimir, ImprimirContagem
from produtos.views import finalizar_contagem, zerar_contagem, ListaDeComprasTotal, TiposDeProdutos, \
    ComprasPorTipo, ContagensRealizadas, ContagemDetalhe

urlpatterns = [
    path('', include('usuarios.urls')),
    path('lojas/', include('lojas.urls')),
    path('produtos/', include('produtos.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
