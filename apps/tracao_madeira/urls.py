from django.urls import path
from .views.views_tracao import FormularioTracaoMadeiraView

from ..compressao_madeira.views import *


#from  .views.view_momento import MomentoVigaPilarView
app_name = "tracao_madeira"

urlpatterns = [
    path('', FormularioTracaoMadeiraView.as_view(), name='form'),

]
