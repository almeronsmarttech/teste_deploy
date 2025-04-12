from allauth.account.adapter import DefaultAccountAdapter
from django.shortcuts import resolve_url

class CustomAccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        """
        Define para onde o usuário será redirecionado após o login.
        """
        return resolve_url("home")

    def get_signup_redirect_url(self, request):
        """
        Define para onde o usuário será redirecionado após o cadastro.
        """
        return resolve_url("loginapp:verify_email")
