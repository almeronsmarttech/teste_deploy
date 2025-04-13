from django.urls import path
#from .views import SomaView
from .views import LajeFormView, AtualizarPView


urlpatterns = [

    #path('', LajePartialView.as_view(), name='laje'),
    path("formulario/", LajeFormView.as_view(), name="laje"),
    path("atualizar-p/", AtualizarPView.as_view(), name="atualizar_p"),
    #path("atualizar-p/", AtualizarPView.as_view(), name="atualizar_p"),
]
