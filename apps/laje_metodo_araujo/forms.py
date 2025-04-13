from django import forms

class LajeForm(forms.Form):
    lx = forms.IntegerField(label="lx (cm)")
    ly = forms.IntegerField(label="ly (cm)")
    h = forms.IntegerField(label="h (cm)")
    g = forms.FloatField(label="g (kN/m²)")
    q = forms.FloatField(label="q (kN/m²)")
    tipo_laje = forms.IntegerField(label="Tipo da Laje (1-6)", min_value=1, max_value=6)
