from django.conf import settings
from django import forms
from django.core.mail.message import EmailMessage
from .models import FlexaoNormalSimplesRetangularModel

class Contato1Form(forms.Form):
    nome = forms.CharField(label='Nome', max_length=100)
    email = forms.EmailField(label='E-mail', max_length=100)
    assunto = forms.CharField(label='Assunto', max_length=100)
    mensagem = forms.CharField(label='Mensagem', widget=forms.Textarea())

    def send_mail(self):
        nome = self.cleaned_data['nome']
        email = self.cleaned_data['email']
        assunto = self.cleaned_data['assunto']
        mensagem = self.cleaned_data['mensagem']

        conteudo = f'Nome: {nome}\nE-mail: {email}\nAssunto: {assunto}\nMensagem: {mensagem}'

        mail = EmailMessage(
            subject=assunto,
            body=conteudo,
            from_email=settings.EMAIL_HOST_USER,
            to=[settings.EMAIL_HOST_USER,],
            headers={'Reply-To': email}
        )
        mail.send()



class FlexaoNormalSimplesRetangularForm(forms.ModelForm):
    class Meta:
        model = FlexaoNormalSimplesRetangularModel
        fields = ['fck', 'fyk', 'es', 'gamac', 'gamas', 'gamaf', 'bduct', 'b', 'h', 'd', 'amk']
        widgets = {
            'fck': forms.Select(attrs={'class': 'form-select'}),
            'fyk': forms.Select(attrs={'class': 'form-select'}),
            'es': forms.Select(attrs={'class': 'form-select'}),
            'gamac': forms.NumberInput(attrs={'class': 'form-control'}),
            'gamas': forms.NumberInput(attrs={'class': 'form-control'}),
            'gamaf': forms.NumberInput(attrs={'class': 'form-control'}),
            'bduct': forms.NumberInput(attrs={'class': 'form-control'}),
            'b': forms.NumberInput(attrs={'class': 'form-control'}),
            'h': forms.NumberInput(attrs={'class': 'form-control'}),
            'd': forms.NumberInput(attrs={'class': 'form-control'}),
            'amk': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'gamac': '&#947;<sub>c</sub>',
            'gamas': '&#947;<sub>s</sub>',
            'gamaf': '&#947;<sub>f</sub>',
            'fck': 'f<sub>ck</sub> (MPa)',
            'fyk': 'f<sub>yk</sub> (MPa)',
            'es': 'E<sub>s</sub> (GPa)',
            'bduct': '&#946;<sub>duct</sub>',
            'b': 'b (cm)',
            'h': 'h (cm)',
            'd': 'd (cm)',
            'amk': 'M<sub>k</sub> (kN.m)',
        }

    def clean(self):
        cleaned_data = super().clean()
        h = cleaned_data.get('h')
        d = cleaned_data.get('d')

        if d is not None and h is not None and d > h:
            self.add_error('d', 'd não pode ser maior que h.')

        return cleaned_data