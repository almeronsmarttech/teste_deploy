from django.views.generic.edit import FormView
from django.shortcuts import render
from apps.pilar_retangular.forms.forms_momento import MomentoVigaPilarForm
from domain.codes.nbr_6118_2023.momento_fletor_viga_pilar import momento_viga_pilar_araujo_viga_continua
#from domain.elements.momento_viga_pilar import MomentoVigaPilar

class MomentoVigaPilarView(FormView):
    template_name = "pilar_retangular/momento_formulario.html"
    form_class = MomentoVigaPilarForm
    success_url = "/pilar/momento/"

    def form_valid(self, form):
        dados = form.cleaned_data

        if dados.get("iguais"):
            dados["lx_sup"] = dados["lx_inf"]
            dados["ly_sup"] = dados["ly_inf"]
            dados["l_sup"] = dados["l_inf"]

        #momento = MomentoVigaPilar(**dados).calcular()
        #momento = 18.22525
        #(l_inf, b_inf, h_inf, l_sup, b_sup, h_sup, l_viga, b_viga, h_viga, q_viga):
        momento = momento_viga_pilar_araujo_viga_continua(dados["l_inf"],dados["lx_inf"], dados["ly_inf"],dados["l_sup"],dados["lx_sup"], dados["ly_sup"],
                                                          dados["l"], dados["b"], dados["h"], dados["q"])

        context = {
            "form": form,
            "resultado": {"momento_transferido": round(momento, 2)},
            "iguais": dados.get("iguais", True)
        }

        if self.request.htmx:
            return render(self.request, "pilar_retangular/momento_resultados.html", context)
        return self.render_to_response(context)