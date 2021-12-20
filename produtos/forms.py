from django import forms


class ProdutoForm(forms.Form):
    qtd = forms.IntegerField(label='', required=True, widget=forms.TextInput(
        attrs={'type': 'number', 'class': 'border-1 form-control text-center qtd',
               'name': 'teste'
               }))
