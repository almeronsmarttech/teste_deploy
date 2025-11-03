from django.urls import path

from .views.views_compressao import FormularioCompressaoMadeiraView

from ..compressao_madeira.views import *


#from  .views.view_momento import MomentoVigaPilarView
app_name = "compressao_madeira"

urlpatterns = [
    path('', FormularioCompressaoMadeiraView.as_view(), name='form'),
    #path('momento/', MomentoVigaPilarView.as_view(), name='momento'),
    #path("desenho-svg/", desenhar_secao_svg, name="desenhar_secao_svg"),

]
