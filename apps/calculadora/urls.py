from django.urls import path
#from .views import SomaView
from .views import CalculadoraView
from .views import form_horizontal

urlpatterns = [
    #path('', home),
    #path('', SomaView.as_view(), name='soma'),
    path('', CalculadoraView.as_view(), name='calculadora'),
    path('form_horizontal', form_horizontal),
]
