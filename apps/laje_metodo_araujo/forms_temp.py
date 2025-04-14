from django import forms

class LajeForm(forms.Form):
    # campos geométricos...
    lx = forms.IntegerField(label="lₓ (cm)")
    ly = forms.IntegerField(label="lᵧ (cm)")
    h = forms.IntegerField(label="h (cm)")
    tipo_laje = forms.IntegerField(label="Tipo da Laje (1–6)", min_value=1, max_value=6)

    # coeficientes
    gama_f = forms.FloatField(label="γf", initial=1.4)
    gama_c = forms.FloatField(label="γc", initial=1.4)
    gama_s = forms.FloatField(label="γs", initial=1.15)

    # materiais e cargas
    fck = forms.ChoiceField(
        label="fck (MPa)",
        choices=[(v, str(v)) for v in range(20, 95, 5)],
        initial=25
    )
    g = forms.FloatField(label="g (kN/m²)")
    q = forms.FloatField(label="q (kN/m²)")
    p = forms.FloatField(label="p = g + q", required=False, disabled=True)
