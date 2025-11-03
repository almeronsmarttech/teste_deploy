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

        # Normalização dos ChoiceFields (strings -> numérico)
        # classe_resistencia: D20..D60 com valores 20,30,40,50,60
        classe_resistencia_val = int(cd["classe_resistencia"])
        # classe_carregamento: Permanente..Instantânea com valores 0.6..1.1
        classe_carregamento_val = float(cd["classe_carregamento"])
        print(f"classe de carregamento {classe_carregamento_val}")
        # Echo dos inputs (útil para rodapé do resultado)
        inputs = {
            "hx": cd["hx"],                    # cm
            "hy": cd["hy"],                    # cm
            "classe_resistencia": classe_resistencia_val,
            "umidade_ambiente": cd["umidade_ambiente"],  # %
            "Nk": cd["Nk"],                    # kN
            "Mkx": cd["Mkx"],                  # kN·m
            "Mky": cd["Mky"],                  # kN·m
            "classe_carregamento": classe_carregamento_val,
        }


        #(self, D=20, u_amb=65, carregamento=1, gama_w_c=1.4, gama_w_t=1.4, gama_w_v=1.8):
        madeira = Madeira(int(classe_resistencia_val), float(cd["umidade_ambiente"]), classe_carregamento_val)
        # def __init__(self: object, hx: int = 2, hy: int = 2, lex: int = 300, ley: int = 300) -> None:
        secao = SecaoRetangular(int(cd["hx"]),int(cd["hy"]))
        # NSk: float = 0, MSkx: float = 0, MSky: float = 0, VSk: float = 0
        acoes = Acoes(float(cd["Nk"]),float(cd["Mkx"]),float(cd["Mky"]))

        # =============================================
        resposta = tracao(madeira, secao, acoes)
        resultados = {
            "ft0d": round(madeira.ft0d, 3),
            "sigma_sd": round(resposta,3),
        }

        # Retorna apenas o fragmento para o alvo HTMX do formulário
        return render(
            self.request,
            "resultados_parciais_tracao.html",
            {"resultados": resultados},
        )

    def form_invalid(self, form):
        # Re-renderiza a página do formulário com os erros (comportamento padrão que você já usa)
        return render(
            self.request,
            self.template_name,
            {"form": form},
            status=400,
        )
