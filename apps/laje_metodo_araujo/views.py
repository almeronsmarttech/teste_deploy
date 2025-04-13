from django.views.generic import FormView
from django.shortcuts import render
from domain.elements.laje import LajeBidirecional
from domain.materials.aco import Aco,Barra
from domain.materials.concreto import Concreto, TipoAgregado
from .forms import LajeForm


class LajeFormView(FormView):
    template_name = "laje_metodo_araujo/laje_formulario.html"
    form_class = LajeForm

    def form_valid(self, form):
        concreto_C25 = Concreto(fck=25, tipo_agregado=TipoAgregado.CALCARIO)
        aco_CA50 = Aco(fyk=500)
        aco_CA60 = Aco(fyk=600)
        bitolas = []
        barra_5mm = Barra(aco_CA60, diametro=5.0)
        bitolas.append(barra_5mm)
        barra_6_3mm = Barra(aco_CA50, diametro=6.3)
        bitolas.append(barra_6_3mm)
        barra_8mm = Barra(aco_CA50, diametro=8.0)
        bitolas.append(barra_8mm)
        dados = form.cleaned_data
        laje = LajeBidirecional(
            lx=dados["lx"]/100,
            ly=dados["ly"]/100,
            h=dados["h"],
            g=dados["g"],
            q=dados["q"],
            tipo_laje=dados["tipo_laje"],
            concreto=concreto_C25,
            aco=aco_CA50,
            bitolas=bitolas,
            psi2=0.3
        )

        resultados = {
            "parametros":laje.calcular_reacoes(),
            "reacoes": laje.calcular_reacoes_apoio(),
            "momentos": laje.calcular_momentos_fletores(),
            "flecha_inicial": laje.calcular_flecha_inicial(),
            "flecha_final": laje.calcular_flecha_final(alfa_f=2.5),
            "calcular_armaduras": laje.calcular_armaduras(),
            "detalhar_armaduras": laje.detalhar_armaduras()
        }

        return render(self.request, "laje_metodo_araujo/resultados_parciais.html", {"resultados": resultados})

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))