from django.views.generic.edit import FormView
from django.shortcuts import render
from apps.pilar_retangular.forms.forms_pilar import PilarRetangularForm
from domain.elements.pilar import PilarRetangular
from domain.structure.estrutura import Estrutura
from domain.materials.concreto import Concreto
from domain.materials.aco import Aco
from django.utils import timezone

class PilarRetangularView(FormView):
    template_name = "pilar_retangular/formulario.html"
    form_class = PilarRetangularForm
    success_url = "/pilar/"

    def form_valid(self, form):
        hx = form.cleaned_data["hx"]
        hy = form.cleaned_data["hy"]
        lex = form.cleaned_data["lex"]
        ley = form.cleaned_data["ley"]
        Nk = form.cleaned_data.get("Nk") or 0
        Mkx_topo = form.cleaned_data.get("Mkx_topo") or 0
        Mkx_base = form.cleaned_data.get("Mkx_base") or 0
        Mky_topo = form.cleaned_data.get("Mky_topo") or 0
        Mky_base = form.cleaned_data.get("Mky_base") or 0

        fck = form.cleaned_data.get("fck", 30)
        fyk = form.cleaned_data.get("fyk", 500)
        caa = form.cleaned_data.get("caa", "I")
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

        pilar = PilarRetangular(
            hx=hx, hy=hy, lex=lex, ley=ley,
            Nk=Nk, Mkx_topo=Mkx_topo, Mkx_base=Mkx_base,
            Mky_topo=Mky_topo, Mky_base=Mky_base,
            estrutura=estrutura
        )


        resultado = pilar.resultados()
        print(pilar)
        context = {
            "form": form,
            "Mdtotx_topo": resultado[0],
            "Mdtotx_base": resultado[1],
            #"Mdtotx_centro": resultado[2],
            #"Mdtoty_topo": resultado[3],
            #"Mdtoty_base": resultado[4],
            #"Mdtoty_centro": resultado[5],
            "timestamp": timezone.now()
        }

        if self.request.htmx:
            return render(self.request, "pilar_retangular/resultados.html", context)
        return self.render_to_response(context)