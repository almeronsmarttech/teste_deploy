from django.urls import path
from .views import ConteudoPartialView

app_name = 'menu1'

urlpatterns = [
    path('conteudo/', ConteudoPartialView.as_view(), name='conteudo_partial'),
]
