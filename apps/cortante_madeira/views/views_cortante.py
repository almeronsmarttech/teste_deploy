from django.views.generic.edit import FormView
from django.shortcuts import render

from domain.elements.acoes import Acoes
from ..forms.forms_cortante import CortanteMadeiraForm

from domain.materials.madeira import Madeira
from domain.elements.secao_transversal import SecaoRetangular
from domain.elements.acoes import Acoes
from domain.codes.nbr_7190_2022.cisalhamento import cisalhamento

class FormularioCisalhamentoMadeiraView(FormView):
    form_class = CortanteMadeiraForm
    template_name = "formulario_cortante.html"

    def form_valid(self, form):
        cd = form.cleaned_data

        classe_resistencia_val = int(cd["classe_resistencia"])      # 20..60
        classe_carregamento_val = float(cd["classe_carregamento"])  # 0.6..1.1

        madeira = Madeira(
            classe_resistencia_val,
            float(cd["umidade_ambiente"]),
            classe_carregamento_val,
        )
        secao = SecaoRetangular(int(cd["b"]), int(cd["h"]))

        # Apenas força cortante (adotei VSk; momentos zero)
        acoes = Acoes(
            0.0,   # NSk
            0.0,   # MSkx
            0.0,   # MSky
            float(cd["Vk"])  # VSk
        )

        # Cálculo no domínio
        resp = cisalhamento(madeira, secao, acoes)

        # τ_d (tald) — tensão de cisalhamento de cálculo
        if isinstance(resp, dict):
            tald = float(resp.get("tald", resp.get("tau_d", 0.0)))
        else:
            tald = float(resp[0]) if (hasattr(resp, "__len__") and len(resp) > 0) else 0.0

        # f_v0d — resistência de cálculo ao cisalhamento paralelo
        fv0d = float(getattr(madeira, "fv0d", 0.0))

        rel = (tald / fv0d) if fv0d else None
        atende = (rel is not None) and (rel <= 1.0)

        resultados = {
            "tald": round(tald, 3),
            "fv0d": round(fv0d, 3),
            "rel": round(rel, 3) if rel is not None else None,
            "atende": atende,
            "inputs": {
                "b": cd["b"], "h": cd["h"],
                "classe_resistencia": classe_resistencia_val,
                "umidade_ambiente": cd["umidade_ambiente"],
                "Vk": cd["Vk"],
                "classe_carregamento": classe_carregamento_val,
            },
        }

        return render(
            self.request,
            "resultados_parciais_cortante.html",
            {"resultados": resultados},
        )

    def form_invalid(self, form):
        return render(
            self.request,
            self.template_name,
            {"form": form},
            status=400,
        )