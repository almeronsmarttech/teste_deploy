from django.views.generic.edit import FormView
from django.shortcuts import render

from domain.elements.acoes import Acoes
from ..forms.forms_flexao import FlexaoMadeiraForm

from domain.materials.madeira import Madeira
from domain.elements.secao_transversal import SecaoRetangular
from domain.elements.acoes import Acoes
from domain.codes.nbr_7190_2022.flexao_simples_reta_obliqua import flexao

class FormularioFlexaoMadeiraView(FormView):
    form_class = FlexaoMadeiraForm
    template_name = "formulario_flexao.html"

    def form_valid(self, form):
        cd = form.cleaned_data

        # Normalização dos ChoiceFields
        classe_resistencia_val = int(cd["classe_resistencia"])      # 20..60
        classe_carregamento_val = float(cd["classe_carregamento"])  # 0.6..1.1

        # Materiais / Seção / Ações
        madeira = Madeira(
            classe_resistencia_val,
            float(cd["umidade_ambiente"]),
            classe_carregamento_val,
        )
        # b, h (cm)
        secao = SecaoRetangular(
            int(cd["b"]),
            int(cd["h"]),
        )
        # Somente momento fletor (adotei Mk em x; ajuste se seu domínio usar outro eixo)
        acoes = Acoes(
            0.0,                      # NSk
            float(cd["Mk"]),          # MSkx
            0.0                       # MSky
        )

        # Cálculo no domínio
        resp = flexao(madeira, secao, acoes)

        # Tensão solicitante de cálculo (σ_Md) e resistência de cálculo à flexão (f_md)
        # Suporte a diferentes formatos de retorno do domínio
        if isinstance(resp, dict):
            sigma_md = float(resp.get("sigma_md", resp.get("sigma_sd", 0.0)))
        else:
            # se o domínio retornar lista/tupla, assumir o primeiro como σ (ajuste se necessário)
            sigma_md = float(resp[0]) if (hasattr(resp, "__len__") and len(resp) > 0) else 0.0

        fmd = madeira.fmd

        # Razão e verificação
        rel = (sigma_md / fmd) if fmd else None
        atende = (rel is not None) and (rel <= 1.0)

        resultados = {
            "sigma_md": round(sigma_md, 3),
            "fmd": round(fmd, 3),
            "rel": round(rel, 3) if rel is not None else None,
            "atende": atende,
            "inputs": {
                "b": cd["b"], "h": cd["h"],
                "classe_resistencia": classe_resistencia_val,
                "umidade_ambiente": cd["umidade_ambiente"],
                "Mk": cd["Mk"],
                "classe_carregamento": classe_carregamento_val,
            },
        }

        return render(
            self.request,
            "resultados_parciais_flexao.html",
            {"resultados": resultados},
        )

    def form_invalid(self, form):
        return render(
            self.request,
            self.template_name,
            {"form": form},
            status=400,
        )