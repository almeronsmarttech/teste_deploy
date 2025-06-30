from django.views.generic.edit import FormView
from django.shortcuts import render
from apps.pilar_retangular.forms.forms_pilar import PilarRetangularForm
from domain.elements.pilar import PilarRetangular
from domain.structure.estrutura import Estrutura
from domain.materials.concreto import Concreto
from domain.materials.aco import Aco
from django.utils import timezone
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_GET
from domain.utils.desenho import desenhar_svg_pilar, desenhar_svg_resultado
from math import pi


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

        # Cálculo das áreas de aço As_x e As_y
        num_barras_x = int(form.cleaned_data.get("num_barras_x", 2))
        num_barras_y = int(form.cleaned_data.get("num_barras_y", 2))
        bitola_mm = float(form.cleaned_data.get("bitola_mm", 10.0))
        area_barra_cm2 = (pi * bitola_mm**2) / 400.0
        As_x = num_barras_x * area_barra_cm2
        As_y = num_barras_y * area_barra_cm2
        print(f"Asx existente= {As_x} cm2\tAs_y existente= {As_y} cm2")

        #print(f"MRdxx = {MRdxx}\tMRdyy = {MRdyy}")
        svg_resultado = desenhar_svg_resultado(
            hx=float(hx),
            hy=float(hy),
            num_barras_x=num_barras_x,
            num_barras_y=num_barras_y,
            e_x=max(pilar.Mdx_topo, pilar.Mdx_base)/pilar.NSd,
            e_y=max(pilar.Mdy_topo, pilar.Mdy_base)/pilar.NSd,
        )
        resultado = pilar.resultados()
        As1_x_nec, As2_x_nec = pilar.dimensionamento(hx, hy,resultado[0])
        As1_y_nec, As2_y_nec = pilar.dimensionamento(hy, hx, resultado[1])
        print(f"As1_y_necessária= {As1_y_nec} cm2\tAs2_y necessária= {As2_y_nec} cm2")
        print(f"As1_x_necessária= {As1_x_nec} cm2\tAs2_x necessária= {As2_x_nec} cm2")

        As_min = pilar.As_min
        As_max = pilar.As_max
        As_total_existente = (num_barras_x+num_barras_y)*area_barra_cm2
        print(f"As min= {As_min} cm2\tAs existente= {As_total_existente} cm2")


        context = {
            "form": form,
            "Mdtotx_topo": resultado[0],
            "Mdtotx_base": resultado[1],
            "hx": hx,
            "hy": hy,
            "num_barras_x": num_barras_x,
            "num_barras_y": num_barras_y,
            "As_x": round(As_x, 2),
            "As_y": round(As_y, 2),
            "bitola_mm": bitola_mm,
            "timestamp": timezone.now(),
            "svg_resultado": svg_resultado,
            "As_x": round(As_x,2),
            "As_y": round(As_y,2),
            "As_x_nec": round(max(As1_x_nec,As2_x_nec),2),
            "As_y_nec": round(max(As1_y_nec,As2_y_nec),2),
            "As_min": round(As_min,2),
            "As_max": round(As_max,2),
            "As_total_existente": round(As_total_existente,2),
        }

        if self.request.htmx:
            return render(self.request, "pilar_retangular/resultados.html", context)
        return self.render_to_response(context)


@require_GET
def desenhar_secao_svg(request):
    try:
        hx = float(request.GET.get("hx", "") or 20)
        hy = float(request.GET.get("hy", "") or 40)
        num_barras_x = int(request.GET.get("num_barras_x", "") or 2)
        num_barras_y = int(request.GET.get("num_barras_y", "") or 2)
        cor_fundo = request.GET.get("cor_fundo", "#FFFFFF")
        cor_barras = request.GET.get("cor_barras", "black")
    except ValueError:
        hx, hy = 20, 40
        num_barras_x, num_barras_y = 2, 2
        cor_fundo, cor_barras = "#FFFFFF", "black"

    svg = desenhar_svg_pilar(hx, hy, num_barras_x, num_barras_y, cor_fundo, cor_barras)
    return HttpResponse(svg, content_type="image/svg+xml")
