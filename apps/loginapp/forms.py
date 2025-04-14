from django.contrib.auth.forms import UserCreationForm
#from .models import CustomUser, Role
# apps/loginapp/forms_temp.py
from django import forms
from django.contrib.auth.models import User

class EmailLoginForm(forms.Form):
    """Formulário para entrada do e-mail"""
    email = forms.EmailField(label="E-mail", widget=forms.EmailInput(attrs={
        "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:ring-blue-500 focus:border-blue-500"
    }))



class VerificationCodeForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:ring-blue-500 focus:border-blue-500",
        "placeholder": "Seu e-mail"
    }))
    verification_code = forms.CharField(required=False, widget=forms.TextInput(attrs={
        "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:ring-blue-500 focus:border-blue-500",
        "placeholder": "Código de verificação"
    }))




class UserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')

        if password != password_confirm:
            raise forms.ValidationError("As senhas não coincidem.")
        return password_confirm

