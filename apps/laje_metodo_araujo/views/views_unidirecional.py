from django.views.generic.edit import FormView
from django.shortcuts import render
from domain.materials.aco import Aco, Barra
from domain.materials.concreto import Concreto, TipoAgregado
from domain.elements.laje import LajeUnidirecional
from ..forms.forms_unidirecional import LajeUnidirecionalForm


class FormularioUnidirecionalView(FormView):
    template_name = "laje_metodo_araujo/unidirecional/formulario.html"
    form_class = LajeUnidirecionalForm

    def form_valid(self, form):
        dados = form.cleaned_data

        concreto = Concreto(
            fck=int(dados["fck"]),
            tipo_agregado=TipoAgregado.CALCARIO
        )

        aco_CA50 = Aco(fyk=500)
        aco_CA60 = Aco(fyk=600)

        bitolas = [
            Barra(aco_CA60, diametro=5.0),
            Barra(aco_CA50, diametro=6.3),
            Barra(aco_CA50, diametro=8.0),
            Barra(aco_CA50, diametro=12.5),
            Barra(aco_CA50, diametro=20.0)
        ]

        laje = LajeUnidirecional(
            lx=dados["lx"] / 100,
            ly=dados["ly"] / 100,
            h=dados["h"],
            g=dados["g"],
            q=dados["q"],
            tipo_laje=dados["tipo_laje"],
            concreto=concreto,
            aco=aco_CA50,
            bitolas=bitolas,
            psi2=dados["psi2"],
        )

        resultados = {
            "reacoes": laje.calcular_reacoes_apoio(),
            "momentos": laje.calcular_momentos_fletores(),
            "flecha_inicial": laje.calcular_flecha_inicial(),
            "flecha_final": laje.calcular_flecha_final(alfa_f=2.5),
            "flecha_limite": laje.calcular_flecha_limite(),
            "calcular_armaduras": laje.calcular_armaduras(),
            "detalhar_armadura_positiva": laje.detalhar_armaduras()[0],
            "detalhar_armadura_negativa": laje.detalhar_armaduras()[1],
            "detalhar_armadura_secundaria": laje.detalhar_armaduras()[2],
        }

        return render(
            self.request,
            "laje_metodo_araujo/unidirecional/resultados_parciais.html",
            {"resultados": resultados}
        )
