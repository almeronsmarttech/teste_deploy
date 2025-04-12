from django.urls import path
#from .views import SomaView
from .views import LajePartialView


urlpatterns = [

    path('', LajePartialView.as_view(), name='laje'),

]
