from django.views.generic import FormView, View
from django.shortcuts import render
from domain.elements.laje import LajeBidirecional
from domain.materials.aco import Aco,Barra
from domain.materials.concreto import Concreto, TipoAgregado
from .forms import LajeForm


class LajeFormView(FormView):
    template_name = "laje_metodo_araujo/laje_formulario.html"
    form_class = LajeForm

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

        laje = LajeBidirecional(
            lx=dados["lx"] / 100,
            ly=dados["ly"] / 100,
            h=dados["h"],
            g=dados["g"],
            q=dados["q"],
            tipo_laje=dados["tipo_laje"],
            concreto=concreto,
            aco=aco_CA50,
            bitolas=bitolas,
            psi2=0.3
        )

        resultados = {
            "parametros": laje.calcular_reacoes(),
            "reacoes": laje.calcular_reacoes_apoio(),
            "momentos": laje.calcular_momentos_fletores(),
            "flecha_inicial": laje.calcular_flecha_inicial(),
            "flecha_final": laje.calcular_flecha_final(alfa_f=2.5),
            "flecha_limite": laje.calcular_flecha_limite(),
            "calcular_armaduras": laje.calcular_armaduras(),
            "detalhar_armaduras": laje.detalhar_armaduras()
        }

        return render(self.request, "laje_metodo_araujo/resultados_parciais.html", {"resultados": resultados})

class AtualizarPView(View):
    def post(self, request):
        form = LajeForm(request.POST)

        try:
            g = float(request.POST.get("g", 0) or 0)
            q = float(request.POST.get("q", 0) or 0)
        except ValueError:
            g = q = 0

        p = round(g + q, 2)

        # Força o valor de p no formulário
        form.fields["p"].initial = p
        form.initial["p"] = p
        form.data = form.data.copy()
        form.data["p"] = p

        return render(request, "laje_metodo_araujo/campo_p.html", {"form": form})