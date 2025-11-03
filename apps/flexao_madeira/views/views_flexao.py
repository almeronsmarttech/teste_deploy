from django.views.generic.edit import FormView
from django.shortcuts import render

from domain.elements.acoes import Acoes
from ..forms.forms_flexao import FlexaoMadeiraForm

from domain.materials.madeira import Madeira
from domain.elements.secao_transversal import SecaoRetangular
from domain.elements.acoes import Acoes
from domain.codes.nbr_7190_2022.compressao_flexo_compressao import compressao

class FormularioFlexaoMadeiraView(FormView):
    form_class = FlexaoMadeiraForm
    template_name = "formulario_flexao.html"

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
            "lx": cd["lx"],                    # cm
            "ly": cd["ly"],                    # cm
            "classe_resistencia": classe_resistencia_val,
            "umidade_ambiente": cd["umidade_ambiente"],  # %
            "Nk": cd["Nk"],                    # kN
            "Mkx": cd["Mkx"],                  # kN·m
            "Mky": cd["Mky"],                  # kN·m
            "classe_carregamento": classe_carregamento_val,
        }

        # ===== PONTO DE INTEGRAÇÃO COM O DOMÍNIO =====
        # Substituir os placeholders abaixo por chamadas reais, ex.:
        # resultados_calc = dominio.calcular(...inputs...)
        # sigma_rd = resultados_calc.sigma_rd
        # ...

        #(self, D=20, u_amb=65, carregamento=1, gama_w_c=1.4, gama_w_t=1.4, gama_w_v=1.8):
        madeira = Madeira(int(classe_resistencia_val), float(cd["umidade_ambiente"]), classe_carregamento_val)
        # def __init__(self: object, hx: int = 2, hy: int = 2, lex: int = 300, ley: int = 300) -> None:
        secao = SecaoRetangular(int(cd["hx"]),int(cd["hy"]),int(cd["lx"]),int(cd["ly"]))
        # NSk: float = 0, MSkx: float = 0, MSky: float = 0, VSk: float = 0
        acoes = Acoes(float(cd["Nk"]),float(cd["Mkx"]),float(cd["Mky"]))


        sigma_rd = 1
        sigma_sd = 1
        sigma_rel = 1
        k = 1
        kc = 1
        # =============================================
        respostas = compressao(madeira, secao, acoes)
        resultados = {
            "sigma_rd": round(madeira.fc0d,3),
            "sigma_sd": round(respostas[0],3),
            "sigma_rel": round(respostas[1],3),
            "k": round(respostas[2],2),
            "kc": round(respostas[3],2),
            "inputs": inputs,
            "ver": round(respostas[4],2),
        }

        # Retorna apenas o fragmento para o alvo HTMX do formulário
        return render(
            self.request,
            "resultados_parciais.html",
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
