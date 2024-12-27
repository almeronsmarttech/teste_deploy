from django.contrib import admin
from django.urls import path, include
from .views import IndexView, Contato1View, CurvaView, FlexaoNormalSimplesRetangularView #,  ContactView

urlpatterns = [
   path('', IndexView.as_view(), name='IndexView'),
   path('curva/', CurvaView.as_view(), name='CurvaView'),
   #path('flexao-normal-simples-retangular/', FlexaoNormalSimplesRetangularView.as_view(), name='FNSR_View'),
   path('flexao-normal-simples-retangular/', FlexaoNormalSimplesRetangularView.as_view(), name='flexao_normal_simples_retangular_view'),
   path('contato/', Contato1View.as_view(), name='ContatoView'),
   # AllAuth Override default postlogin action with our view
   path('accounts/profile/', IndexView.as_view(), name='profileOverridenView'),
   path('calculadora/', include('apps.calculadora.urls')),
]