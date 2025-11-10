from django.views.generic.edit import FormView
from django.shortcuts import render

from domain.elements.acoes import Acoes
from ..forms.forms_tracao import TracaoMadeiraForm

from domain.materials.madeira import Madeira
from domain.elements.secao_transversal import SecaoRetangular
from domain.elements.acoes import Acoes
from domain.codes.nbr_7190_2022.tracao_flexo_tracao import tracao

class FormularioTracaoMadeiraView(FormView):
    form_class = TracaoMadeiraForm
    template_name = "formulario_tracao.html"

    def form_valid(self, form):
        cd = form.cleaned_data

        # Normalização dos ChoiceFields
        classe_resistencia_val = int(cd["classe_resistencia"])      # 20..60
        classe_carregamento_val = float(cd["classe_carregamento"])  # 0.6..1.1

        # Materiais / Seção / Ações
        madeira = Madeira(
            int(classe_resistencia_val),
            float(cd["umidade_ambiente"]),
            classe_carregamento_val
        )

        secao = SecaoRetangular(
            int(cd["hx"]),  # usando hx como dimensão x
            int(cd["hy"]),  # e hy como dimensão y
        )

        # Furos na seção (opcional)
        n_furos = int(cd.get("numero_furos", 0) or 0)
        diam_cm = float(cd.get("diametro_furo", 0.0) or 0.0)
        if n_furos > 0 and diam_cm > 0:
            if hasattr(secao, "set_furos"):
                try:
                    secao.set_furos(n=n_furos, diametro_cm=diam_cm)
                except Exception:
                    pass
            else:
                secao.furos = {"n": n_furos, "diametro_cm": diam_cm}

        acoes = Acoes(
            float(cd["Nk"]),   # NSk (kN)
            float(cd["Mkx"]),  # MSkx (kN·m)
            float(cd["Mky"]),  # MSky (kN·m)
        )

        # Cálculo (domínio)
        # retorno esperado: sigma_sd (tensão solicitante) — ajuste se sua função retornar múltiplos valores
        resp = tracao(madeira, secao, acoes)

        # if isinstance(resp, dict):
        #     sigma_sd = float(resp.get("sigma_sd", 0.0))
        # else:
        #     # se vier lista/tupla, pegue o primeiro como σ_sd (ajuste se necessário)
        #     sigma_sd = float(resp[0]) if (hasattr(resp, "__len__") and len(resp) > 0) else 0.0
        sigma_sd = resp
        # Resistência de cálculo à tração paralela (f_t0d) vinda do material
        ft0d = madeira.ft0d

        sigma_rel = (sigma_sd / ft0d) if ft0d else None
        atende = (sigma_rel is not None) and (sigma_rel <= 1.0)

        resultados = {
            "sigma_rd": round(ft0d, 3),        # f_t0d
            "sigma_sd": round(sigma_sd, 3),    # solicitante
            "sigma_rel": round(sigma_rel, 3) if sigma_rel is not None else None,
            "atende": atende,
            "inputs": {
                "hx": cd["hx"], "hy": cd["hy"],
                "classe_resistencia": classe_resistencia_val,
                "umidade_ambiente": cd["umidade_ambiente"],
                "Nk": cd["Nk"], "Mkx": cd["Mkx"], "Mky": cd["Mky"],
                "classe_carregamento": classe_carregamento_val,
                "numero_furos": n_furos,
                "diametro_furo": diam_cm,
            },
        }

        return render(
            self.request,
            "resultados_parciais_tracao.html",
            {"resultados": resultados},
        )

    def form_invalid(self, form):
        return render(
            self.request,
            self.template_name,
            {"form": form},
            status=400,
        )