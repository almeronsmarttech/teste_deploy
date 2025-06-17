from django import forms

class MomentoVigaPilarForm(forms.Form):
    # Pilar inferior
    lx_inf = forms.FloatField(label="lx inferior (cm)")
    ly_inf = forms.FloatField(label="ly inferior (cm)")
    l_inf = forms.FloatField(label="Comprimento inferior (cm)")

    iguais = forms.BooleanField(label="Lance superior igual ao inferior", required=False, initial=True)

    # Pilar superior (será ocultado via lógica condicional)
    lx_sup = forms.FloatField(label="lx superior (cm)", required=False)
    ly_sup = forms.FloatField(label="ly superior (cm)", required=False)
    l_sup = forms.FloatField(label="Comprimento superior (cm)", required=False)

    # Viga
    b = forms.FloatField(label="Largura da viga (cm)")
    h = forms.FloatField(label="Altura da viga (cm)")
    l = forms.FloatField(label="Vão da viga (cm)")
    q = forms.FloatField(label="Carga distribuída q (kN/m)")