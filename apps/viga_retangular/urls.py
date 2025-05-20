from django.urls import path
from .views.view_viga import VigaRetangularView

app_name = 'viga_retangular'

urlpatterns = [
    path('', VigaRetangularView.as_view(), name='formulario'),
]
