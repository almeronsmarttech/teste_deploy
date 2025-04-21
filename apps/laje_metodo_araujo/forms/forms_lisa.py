from django import forms
from domain.materials.concreto import Concreto
from domain.enums import TipoPilarEnum


TIPO_PILAR_CHOICES = [
    (TipoPilarEnum.INTERIOR.value, "Pilar de Interior"),
    (TipoPilarEnum.BORDA.value, "Pilar de Borda"),
    (TipoPilarEnum.CANTO.value, "Pilar de Canto"),
]


class LajeLisaForm(forms.Form):
    fck = forms.ChoiceField(
        label="fck (MPa)",
        choices=[(f, f) for f in range(20, 95, 5)],
        widget=forms.Select(attrs={"class": "w-full appearance-none"})
    )

    h = forms.IntegerField(
        label="Altura da Laje (cm)",
        min_value=10,
        widget=forms.NumberInput(attrs={"class": "w-full"})
    )

    Ai = forms.FloatField(
        label="Área de Influência (m²)",
        min_value=0.1,
        widget=forms.NumberInput(attrs={"class": "w-full"})
    )

    qmedio = forms.FloatField(
        label="Carga Média (kN/m²)",
        min_value=0.1,
        widget=forms.NumberInput(attrs={"class": "w-full"})
    )

    C1 = forms.FloatField(
        label="C1 - Lado do Pilar Perpendicular ao Bordo da Laje (cm)",
        min_value=0.1,
        widget=forms.NumberInput(attrs={"class": "w-full"})
    )

    C2 = forms.FloatField(
        label="C2 - Lado do Pilar Paralelo ao Bordo da Laje (cm)",
        min_value=0.1,
        widget=forms.NumberInput(attrs={"class": "w-full"})
    )

    tipo_pilar = forms.ChoiceField(
        label="Tipo de Pilar",
        choices=TIPO_PILAR_CHOICES,
        widget=forms.Select(attrs={"class": "w-full appearance-none"})
    )
