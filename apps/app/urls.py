from django.contrib import admin
from django.urls import path, include
from .views import IndexView

urlpatterns = [
   path('', IndexView.as_view(), name='IndexView'),
   #path('calculate/', IndexView.as_view(), name='calculate'),
]