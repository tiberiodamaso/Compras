from django import forms

from .models import Produto


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['qtd']
        widgets = {
            'qtd': forms.TextInput(attrs={'class': 'input border-1 form-control text-center qtd'})
        }
