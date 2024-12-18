from django.views.generic import FormView
from django.shortcuts import render
from .forms import OperacaoForm
import numpy as np

class CalculadoraView(FormView):
    template_name = 'calculadora/calculadora.html'
    form_class = OperacaoForm

    def realizar_operacao(self, numero1, numero2, operacao):
        try:
            operacoes = {
                "soma": numero1 + numero2,
                "subtracao": numero1 - numero2,
                "multiplicacao": numero1 * numero2,
                "divisao": numero1 / numero2 if numero2 != 0 else "Erro: Divisão por zero",
                "exponenciacao": numero1 ** numero2 if numero1 ** numero2 < 1e6 else "Erro: Exponenciação muito grande",
                "radiciacao": numero1 ** (1 / numero2) if numero2 != 0 else "Erro: Radiciação inválida",
                "media": np.mean([numero1,numero2]),
            }
            return operacoes.get(operacao, "Operação inválida")
        except OverflowError:
            return "Erro: Resultado muito grande"

    def form_valid(self, form):
        # Obtendo os números e operação
        numero1 = form.cleaned_data['numero1']
        numero2 = form.cleaned_data['numero2']
        operacao = form.cleaned_data['operacao']

        # Realizando a operação escolhida
        resultado = self.realizar_operacao(numero1, numero2, operacao)

        # Renderizando o template com o resultado
        return render(self.request, self.template_name, {
            'form': form,
            'resultado': resultado,
            'operacao': operacao,
        })


def form_horizontal(request):
    #return render(request,'core/index.html')
    return render(request, 'calculadora/form_horizontal.html')