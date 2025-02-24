from django.urls import path
from .views import ConteudoPartialView

app_name = 'menu2'

urlpatterns = [
    path('conteudo/', ConteudoPartialView.as_view(), name='conteudo_partial'),
]
