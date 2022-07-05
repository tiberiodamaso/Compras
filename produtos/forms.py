from django import forms


class ProdutoForm(forms.Form):
    qtd = forms.FloatField(label='', required=True, widget=forms.TextInput(
        attrs={'type': 'number', 'class': 'border-1 form-control text-center qtd'}))


class PlanilhaForm(forms.Form):
    planilha = forms.FileField(label='', required=True, widget=forms.TextInput(
        attrs={'type': 'file', 'class': 'form-control', 'placeholder': 'Escolha a planilha com produtos',
               'pattern': '^.+\.(xlsx|xls|csv)$', 'accept': 'text/csv, .csv'}
    ))
