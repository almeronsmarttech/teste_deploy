from django.urls import path
#from .views import SomaView
from .views.views_bidirecional import LajeFormView, AtualizarPView
from .views.views_unidirecional  import FormularioUnidirecionalView

urlpatterns = [

    #path('', LajePartialView.as_view(), name='laje'),
    path("formulario/", LajeFormView.as_view(), name="laje"),
    path("atualizar-p/", AtualizarPView.as_view(), name="atualizar_p"),
    path("unidirecional/", FormularioUnidirecionalView.as_view(), name="laje_unidirecional"),
    path("bidirecional/", LajeFormView.as_view(), name="laje_bidirecional"),
]
