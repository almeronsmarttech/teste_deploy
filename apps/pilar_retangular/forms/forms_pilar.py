from django import forms
num_choices = [(i, i) for i in range(2, 11)]


class PilarRetangularForm(forms.Form):
    hx = forms.IntegerField(label='hx (cm)')
    hy = forms.IntegerField(label='hy (cm)')
    lex = forms.IntegerField(label='lex (cm)')
    ley = forms.IntegerField(label='ley (cm)')
    Nk = forms.FloatField(label='Nk (kN)')
    Mkx_topo = forms.FloatField(label='Mkx Topo (kN·m)', required=False)
    Mkx_base = forms.FloatField(label='Mkx Base (kN·m)', required=False)
    Mky_topo = forms.FloatField(label='Mky Topo (kN·m)', required=False)
    Mky_base = forms.FloatField(label='Mky Base (kN·m)', required=False)

    fck = forms.ChoiceField(choices=[(v, v) for v in [20, 25, 30, 35, 40]], label='fck (MPa)', initial=25)
    fyk = forms.ChoiceField(choices=[(500, 500), (600, 600)], label='fyk (MPa)', initial=500)
    caa = forms.ChoiceField(choices=[('I', 'I'), ('II', 'II'), ('III', 'III'), ('IV', 'IV')], label='CAA', initial='II')
    gama_f = forms.FloatField(label='γ_F', initial=1.4)
    gama_c = forms.FloatField(label='γ_c', initial=1.4)
    gama_s = forms.FloatField(label='γ_s', initial=1.15)

    num_barras_x = forms.ChoiceField(label="Nº barras em x", choices=num_choices, initial=2)
    num_barras_y = forms.ChoiceField(label="Nº barras em y", choices=num_choices, initial=2)