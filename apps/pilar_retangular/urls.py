from django.urls import path
from .views.view_pilar import PilarRetangularView, desenhar_secao_svg#, desenhar_secao_colorida
from  .views.view_momento import MomentoVigaPilarView

app_name = 'pilar_retangular'

urlpatterns = [
    path('', PilarRetangularView.as_view(), name='formulario'),
    path('momento/', MomentoVigaPilarView.as_view(), name='momento'),
    path("desenho-svg/", desenhar_secao_svg, name="desenhar_secao_svg"),
    #path("desenhar-secao-colorida/", desenhar_secao_colorida, name="desenhar_secao_colorida"),
]
