from django import forms

class OperacaoForm(forms.Form):
    numero1 = forms.FloatField(label="Número 1", widget=forms.NumberInput(attrs={'class': 'form-control'}))
    numero2 = forms.FloatField(label="Número 2", widget=forms.NumberInput(attrs={'class': 'form-control'}))
    operacao = forms.CharField(widget=forms.HiddenInput(), initial="soma")
