from django.views.generic.edit import FormView
from django.shortcuts import render
from ..forms.forms_lisa import LajeLisaForm
from domain.elements.laje import LajeLisa
from domain.materials.concreto import Concreto, TipoAgregado
from domain.enums import TipoPilarEnum#, TipoAgregado


class LajeLisaFormView(FormView):
    template_name = "laje_metodo_araujo/lisa/laje_lisa_formulario.html"
    form_class = LajeLisaForm

    def form_valid(self, form):
        dados = form.cleaned_data

        concreto = Concreto(
            fck=int(dados["fck"]),
            tipo_agregado=TipoAgregado.CALCARIO
        )

        laje = LajeLisa(
            h=dados["h"],
            concreto=concreto,
            Ai=dados["Ai"],
            qmedio=dados["qmedio"],
            C1=dados["C1"],
            C2=dados["C2"],
            tipo_pilar=TipoPilarEnum(dados["tipo_pilar"])
        )

        resultados = laje.calcular_puncao()

        return render(
            self.request,
            "laje_metodo_araujo/lisa/resultados_laje_lisa.html",
            {"resultados": resultados}
        )
