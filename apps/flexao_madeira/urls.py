from django.urls import path

from .views.views_flexao import FormularioFlexaoMadeiraView

from ..flexao_madeira.views import *


#from  .views.view_momento import MomentoVigaPilarView
app_name = "flexao_madeira"

urlpatterns = [
    path('', FormularioFlexaoMadeiraView.as_view(), name='form'),

]
