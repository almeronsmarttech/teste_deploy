from django import forms

class LajeUnidirecionalForm(forms.Form):
    lx = forms.IntegerField(label="lₓ (cm)", min_value=1)
    ly = forms.IntegerField(label="lᵧ (cm)", min_value=1)
    h = forms.IntegerField(label="h (cm)", min_value=1)
    g = forms.FloatField(label="g (kN/m²)", min_value=0)
    q = forms.FloatField(label="q (kN/m²)", min_value=0)

    tipo_laje = forms.ChoiceField(
        label="Tipo da Laje (1–4)",
        choices=[
            (1, "Tipo 1 – Boros simplesmente apoiados"),
            (2, "Tipo 2 – Um bordo apoiado e outro engastado"),
            (3, "Tipo 3 – Dois bordos engastados"),
            (4, "Tipo 4 – Um bordo engastado e outro em balanço"),
        ],
        initial=1
    )

    gama_f = forms.FloatField(label="γᶠ", initial=1.4)
    gama_c = forms.FloatField(label="γᶜ", initial=1.4)
    gama_s = forms.FloatField(label="γˢ", initial=1.15)

    fck = forms.ChoiceField(
        label="fck (MPa)",
        choices=[(i, str(i)) for i in range(20, 95, 5)],
        initial=25
    )
    fyk = forms.ChoiceField(
        label="fyk (MPa)",
        choices=[(500, "500"), (600, "600")],
        initial=500
    )

    p = forms.FloatField(label="p = g + q", required=False)
    psi2 = forms.FloatField(label="ψ₂", min_value=0, max_value=1, initial=0.3)
