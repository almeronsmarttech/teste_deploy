from django.contrib import admin
from django.urls import path, include
from .views import indexView

urlpatterns = [
   path('', indexView.as_view(), name='IndexView'),
   # AllAuth Override default postlogin action with our view
   path('accounts/profile/', indexView.as_view(), name='profileOverridenView'),
   path('calculadora/', include('apps.calculadora.urls')),
]