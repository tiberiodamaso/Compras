from django.urls import path

from departamentos.views import DepartamentoListView

urlpatterns = [
    path('', DepartamentoListView.as_view(), name='list'),
]
