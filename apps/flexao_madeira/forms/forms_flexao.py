from django import forms

class FlexaoMadeiraForm(forms.Form):
    # --- seus campos exatamente como já estão ---
    b = forms.IntegerField(label="b (cm)", min_value=1)
    h = forms.IntegerField(label="h (cm)", min_value=1)

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

    umidade_ambiente = forms.FloatField(label="Umidade ambiente (%)", min_value=0, max_value=100)

    Mk  = forms.FloatField(label="Mₖ (kN.m)",   min_value=0)

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

    # >>> ADICIONE ESTE __init__ <<<
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        base = "w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
        for name, field in self.fields.items():
            css = base
            step = None

            if isinstance(field.widget, forms.Select):
                # remove seta duplicada e mantém aparência consistente
                field.widget.attrs["class"] = f"{base} appearance-none"
            else:
                # números mais “finos”
                if isinstance(field, (forms.FloatField, forms.IntegerField)):
                    step = "0.01" if isinstance(field, forms.FloatField) else "1"
                field.widget.attrs["class"] = css
                if step:
                    field.widget.attrs["step"] = step
