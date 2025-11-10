from django.urls import path

from .views.views_cortante import FormularioCisalhamentoMadeiraView

from ..compressao_madeira.views import *


#from  .views.view_momento import MomentoVigaPilarView
app_name = "cortante_madeira"

urlpatterns = [
    path('', FormularioCisalhamentoMadeiraView.as_view(), name='form'),

]
