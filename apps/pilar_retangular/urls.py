from django.urls import path
from .views.view_pilar import PilarRetangularView
from  .views.view_momento import MomentoVigaPilarView

app_name = 'pilar_retangular'

urlpatterns = [
    path('', PilarRetangularView.as_view(), name='formulario'),
    path('momento/', MomentoVigaPilarView.as_view(), name='momento'),
]
