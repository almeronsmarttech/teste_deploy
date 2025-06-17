from django import forms

class VigaRetangularForm(forms.Form):
    # Campos principais (visíveis)
    bw = forms.FloatField(label="Largura bw (cm)", min_value=1)
    h = forms.FloatField(label="Altura h (cm)", min_value=1)
    Mk = forms.FloatField(label="Momento solicitante Mk (kN·m)", min_value=0, required=False)
    Vk = forms.FloatField(label="Cortante solicitante Vk (kN)", min_value=0, required=False)

    # Parâmetros avançados (colapsados)
    fck = forms.ChoiceField(
        label="fck (MPa)", choices=[(20, 20), (25, 25), (30, 30), (35, 35), (40, 40), (45, 45), (50, 50),
                                    (55, 55), (60, 60), (65, 65), (70, 70), (75, 75), (80, 80), (85, 85), (90, 90)], initial=25, required=False
    )
    fyk = forms.ChoiceField(
        label="fyk (MPa)", choices=[(500, 500), (600, 600)], initial=500, required=False
    )
    caa = forms.ChoiceField(
        label="CAA", choices=[("I", "I"), ("II", "II"), ("III", "III"), ("IV", "IV")], initial="II", required=False
    )

    gama_f = forms.FloatField(label="γ_F", initial=1.4, required=False)
    gama_c = forms.FloatField(label="γ_c", initial=1.4, required=False)
    gama_s = forms.FloatField(label="γ_s", initial=1.15, required=False)
