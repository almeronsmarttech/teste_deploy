from django.urls import path
#from .views import SomaView
from .views import LajeFormView


urlpatterns = [

    #path('', LajePartialView.as_view(), name='laje'),
    path("formulario/", LajeFormView.as_view(), name="laje"),
]
