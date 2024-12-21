from django.contrib import admin
from django.urls import path, include
from .views import IndexView, Contato1View #,  ContactView

urlpatterns = [
   path('', IndexView.as_view(), name='IndexView'),
   path('contato/', Contato1View.as_view(), name='ContatoView'),
   # AllAuth Override default postlogin action with our view
   path('accounts/profile/', IndexView.as_view(), name='profileOverridenView'),
   path('calculadora/', include('apps.calculadora.urls')),
]