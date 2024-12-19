from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView

# Create your views here.
class indexView(TemplateView):
    template_name = "app/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Verifica se o usuário está autenticado
        if self.request.user.is_authenticated:
            #context['message'] = f"Bem-vindo, {self.request.user.username}! Você está logado."
            context['logado'] = True
        else:
            context['logado'] = False
            #context['message'] = "Você não está logado."
        return context