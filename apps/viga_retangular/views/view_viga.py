from django.views.generic.edit import FormView
from django.shortcuts import render
from apps.viga_retangular.forms.forms_viga import VigaRetangularForm
from domain.elements.viga import VigaRetangular
from domain.structure.estrutura import Estrutura
from domain.materials.concreto import Concreto
from domain.materials.aco import Aco
from django.utils import timezone


class VigaRetangularView(FormView):
    template_name = "viga_retangular/formulario.html"
    form_class = VigaRetangularForm
    success_url = "/viga/"

    def form_valid(self, form):
        bw = form.cleaned_data["bw"]
        h = form.cleaned_data["h"]
        Mk = form.cleaned_data.get("Mk") or 0
        Vk = form.cleaned_data.get("Vk") or 0

        fck = form.cleaned_data.get("fck", 30)
        fyk = form.cleaned_data.get("fyk", 500)
        caa = form.cleaned_data.get("caa", "I")
        psi2 = form.cleaned_data.get("psi2", 0.3)
        gama_f = form.cleaned_data.get("gama_f", 1.4)
        gama_c = form.cleaned_data.get("gama_c", 1.4)
        gama_s = form.cleaned_data.get("gama_s", 1.15)

        concreto = Concreto(fck=fck, gama_c=gama_c)
        aco = Aco(fyk=fyk)

        estrutura = Estrutura(
            concreto=concreto,
            aco=aco,
            caa=caa,
            gama_F=gama_f,
            gama_c=gama_c,
            gama_s=gama_s
        )

        viga = VigaRetangular(bw=bw, h=h, estrutura=estrutura)

        resultados = {}
        if Mk > 0:
            #resultados["As"] = round(viga.calcular_As(Mk), 2)
            as_resultado = viga.calcular_As(Mk)
            #resultados["armaduras_flexao"] = viga.detalhar_As()
            if isinstance(as_resultado, str):
                resultados["mensagem"] = as_resultado
            else:
                as1 = round(as_resultado[0], 2)
                as2 = round(as_resultado[1], 2)
                resultados["As"] = as1
                resultados["As1"] = as2
                resultados["armaduras_flexao"] = viga.detalhar_As1(as1)
                resultados["armaduras_compressao"] = viga.detalhar_As_compressao1(as2)
            print("Era pra chamar o método detalhar As")

        if Vk > 0:
            asw = round(viga.calcular_Asw(Vk), 2)
            resultados["Asw"] = asw
            #resultados["armaduras_cisalhamento"] = viga.detalhar_Asw1(asw)
            resultados["armaduras_cisalhamento"] = viga.detalhar_Asw()
            print("Era pra chamar o método detalhar Asw")
        if not resultados:
            resultados["mensagem"] = "Nenhum esforço fornecido. Informe Mk e/ou Vk."

        context = {
            "form": form,
            "resultados": resultados,
            "timestamp": timezone.now()
        }

        if self.request.htmx:
            return render(self.request, "viga_retangular/resultados.html", context)
        return self.render_to_response(context)
