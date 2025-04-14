from django.views.generic.edit import FormView
from django.shortcuts import render

from domain.materials.aco import Aco, Barra
from ..forms.forms_unidirecional import LajeUnidirecionalForm
from domain.elements.laje import LajeUnidirecional
from domain.materials.concreto import Concreto, TipoAgregado

class FormularioUnidirecionalView(FormView):
    template_name = "laje_metodo_araujo/unidirecional/formulario.html"
    form_class = LajeUnidirecionalForm

    def form_valid(self, form):
        dados = form.cleaned_data

        concreto = Concreto(
            fck=int(dados["fck"]),
            tipo_agregado=TipoAgregado.CALCARIO  # ou tornar isso também um campo se desejar
        )

        aco_CA50 = Aco(fyk=500)
        aco_CA60 = Aco(fyk=600)

        bitolas = [
            Barra(aco_CA60, diametro=5.0),
            Barra(aco_CA50, diametro=6.3),
            Barra(aco_CA50, diametro=8.0),
        ]

        laje = LajeUnidirecional(
            lx=dados["lx"]/100,
            ly=dados["ly"]/100,
            h=dados["h"],
            g=dados["g"],
            q=dados["q"],
            #tipo_laje=dados["tipo_laje"],
            tipo_laje=1,
            concreto=concreto,
            aco=aco_CA50,
            bitolas=bitolas,
            psi2=["psi2"]
            # ... adicione os outros parâmetros conforme necessário
        )



        resultados = {
            "parametros": laje.calcular_reacoes(),
            "reacoes": laje.calcular_reacoes_apoio(),
            "momentos": laje.calcular_momentos_fletores(),
            "flecha_inicial": laje.calcular_flecha_inicial(),
            "flecha_final": laje.calcular_flecha_final(alfa_f=2.5),
            "flecha_limite": laje.calcular_flecha_limite(),
        }

        return render(self.request, "laje_metodo_araujo/unidirecional/resultados_parciais.html", {"resultados": resultados, "form": form})
