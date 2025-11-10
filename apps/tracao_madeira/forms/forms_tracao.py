from django import forms

class TracaoMadeiraForm(forms.Form):
    # Geometria (cm)
    hx = forms.IntegerField(label="hₓ (cm)", min_value=1)
    hy = forms.IntegerField(label="hᵧ (cm)", min_value=1)

    # Classe de resistência (D20..D60 → 20..60)
    CLASSE_RESISTENCIA_CHOICES = [
        (20, "D20"),
        (30, "D30"),
        (40, "D40"),
        (50, "D50"),
        (60, "D60"),
    ]
    classe_resistencia = forms.ChoiceField(
        label="Classe de resistência", choices=CLASSE_RESISTENCIA_CHOICES
    )

    # Ambiente
    umidade_ambiente = forms.FloatField(label="Umidade ambiente (%)", min_value=0, max_value=100)

    # Ações (kN, kN·m)
    Nk  = forms.FloatField(label="Nₖ (kN)",    min_value=0)
    Mkx = forms.FloatField(label="Mₖₓ (kN·m)", min_value=0)
    Mky = forms.FloatField(label="Mₖᵧ (kN·m)", min_value=0)

    # Classe de carregamento (0.6..1.1)
    CLASSE_CARREGAMENTO_CHOICES = [
        (0.6, "Permanente"),
        (0.7, "Longa duração"),
        (0.8, "Média duração"),
        (0.9, "Curta duração"),
        (1.1, "Instantânea"),
    ]
    classe_carregamento = forms.ChoiceField(
        label="Classe de carregamento", choices=CLASSE_CARREGAMENTO_CHOICES
    )

    # Furos na seção
    numero_furos = forms.IntegerField(label="Número de furos", min_value=0, initial=0)
    diametro_furo = forms.FloatField(label="Diâmetro dos furos (cm)", min_value=0.0, initial=0.0)

    # Estilização
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        base = "w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
        for _, field in self.fields.items():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs["class"] = f"{base} appearance-none"
            else:
                field.widget.attrs["class"] = base
                if isinstance(field, forms.FloatField):
                    field.widget.attrs["step"] = "0.01"
                if isinstance(field, forms.IntegerField):
                    field.widget.attrs["step"] = "1"
