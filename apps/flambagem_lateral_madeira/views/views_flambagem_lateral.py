from django.views.generic.edit import FormView
from django.shortcuts import render

from ..forms.forms_flambagem_lateral import FlambagemLateralMadeiraForm

from domain.materials.madeira import Madeira
from domain.elements.secao_transversal import SecaoRetangular
# Se precisar de Acoes no futuro, importe aqui
from domain.elements.acoes import Acoes

# AJUSTAR este import conforme seu domínio:
# exemplo de caminho: domain.codes.nbr_7190_2022.flambagem_lateral import flambagem_lateral
from domain.codes.nbr_7190_2022.flambagem_lateral import flambagem_lateral  # <- ajuste

class FormularioFlambagemLateralMadeiraView(FormView):
    form_class = FlambagemLateralMadeiraForm
    template_name = "formulario_flambagem_lateral.html"

    def form_valid(self, form):
        cd = form.cleaned_data

        # Normalização
        classe_resistencia_val = int(cd["classe_resistencia"])      # 20..60
        classe_carregamento_val = float(cd["classe_carregamento"])  # 0.6..1.1

        # Material e seção
        madeira = Madeira(
            classe_resistencia_val,
            float(cd["umidade_ambiente"]),
            classe_carregamento_val,
        )
        secao = SecaoRetangular(int(cd["b"]), int(cd["h"]))

        # Comprimento efetivo informado
        L1 = int(cd["L1"])

        # === Domínio: retorna exatamente (primeira_parte, segunda_parte) ===
        primeira_parte, segunda_parte = flambagem_lateral(L1,madeira, secao.hx, secao.hy,  acoes = Acoes(0,0,0,0))

        # Conversões e verificação
        try:
            parte1 = float(primeira_parte)
        except Exception:
            parte1 = None

        try:
            parte2 = float(segunda_parte)
        except Exception:
            parte2 = None

        passou = (parte1 is not None and parte2 is not None) and (parte1 <= parte2)
        rel = (parte1 / parte2) if (parte1 is not None and parte2 not in (None, 0)) else None

        resultados = {
            "inputs": {
                "b": cd["b"],
                "h": cd["h"],
                "L1": cd["L1"],
                "classe_resistencia": classe_resistencia_val,
                "umidade_ambiente": cd["umidade_ambiente"],
                "classe_carregamento": classe_carregamento_val,
            },
            "parte1": round(parte1, 3) if parte1 is not None else None,
            "parte2": round(parte2, 3) if parte2 is not None else None,
            "rel": round(rel, 3) if rel is not None else None,
            "passou": passou,
        }

        return render(
            self.request,
            "resultados_parciais_flambagem_lateral.html",
            {"resultados": resultados},
        )

    def form_invalid(self, form):
        return render(
            self.request,
            self.template_name,
            {"form": form},
            status=400,
        )