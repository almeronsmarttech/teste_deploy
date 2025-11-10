from django.urls import path
from .views.views_flambagem_lateral import FormularioFlambagemLateralMadeiraView

app_name = "flambagem_lateral_madeira"

urlpatterns = [
    path("", FormularioFlambagemLateralMadeiraView.as_view(), name="form"),
]
