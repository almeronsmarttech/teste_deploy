from django import forms
from django.utils.safestring import mark_safe


class LajeUnidirecionalForm(forms.Form):
    lx = forms.IntegerField(label="lₓ (cm)", min_value=1)
    ly = forms.IntegerField(label="lᵧ (cm)", min_value=1)
    h = forms.IntegerField(label="h (cm)", min_value=1)
    g = forms.FloatField(label="g (kN/m²)", min_value=0)
    q = forms.FloatField(label="q (kN/m²)", min_value=0)

    tipo_laje = forms.IntegerField(label="Tipo da Laje (1–4)", min_value=1, max_value=4)

    gama_f = forms.FloatField(label=mark_safe("γ<sub>F</sub>"), initial=1.4)
    gama_c = forms.FloatField(label=mark_safe("γ<sub>c</sub>"), initial=1.4)
    gama_s = forms.FloatField(label=mark_safe("γ<sub>s</sub>"), initial=1.15)

    fck = forms.ChoiceField(
        label="fck (MPa)",
        choices=[(i, str(i)) for i in range(20, 95, 5)],
        initial=25
    )
    #fyk = forms.ChoiceField(
    #    label="fyk (MPa)",
    #    choices=[(500, "500"), (600, "600")],
    #    initial=500
    #)

    p = forms.FloatField(label="p = g + q", required=False)
    psi2 = forms.FloatField(label="ψ₂", min_value=0, max_value=1, initial=0.3)

    CAA_CHOICES = [
        ('I', 'Classe I - Fraca'),
        ('II', 'Classe II - Moderada'),
        ('III', 'Classe III - Forte'),
        ('IV', 'Classe IV - Muito forte'),
    ]

    classe_agressividade_ambiental = forms.ChoiceField(
        choices=CAA_CHOICES,
        label="Classe de Agressividade Ambiental (CAA)",
        widget=forms.Select(attrs={"class": "appearance-none w-full p-2 border border-gray-300 rounded"})
    )
