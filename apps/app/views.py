from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView
from pyexpat.errors import messages
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

from .forms import Contato1Form

# Create your views here.
class IndexView(TemplateView):
    template_name = "app/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Verifica se o usuário está autenticado
        if self.request.user.is_authenticated:
            #context['message'] = f"Bem-vindo, {self.request.user.username}! Você está logado."
            context['logado'] = True
            context['nome_completo'] = self.request.user.first_name + " " + self.request.user.last_name
        else:
            context['logado'] = False
            #context['message'] = "Você não está logado."
        return context


class Contato1View(FormView):
    template_name = 'app/contato.html'
    form_class = Contato1Form
    success_url = reverse_lazy('ContatoView')

    def get_context_data(self, **kwargs):
        context = super(Contato1View, self).get_context_data(**kwargs)
        context['latitude'] = -29.1662
        context['longititude'] = -51.1797
        return context

    def form_valid(self, form, *args, **kwargs):
        form.send_mail()
        messages.success(self.request, 'E-mail enviado com sucesso')
        return super(Contato1View, self).form_valid(form, *args, **kwargs)

    def form_invalid(self, form, *args, **kwargs):
        messages.error(self.request, 'Erro ao enviar e-mail')
        return super(Contato1View, self).form_invalid(form, *args, **kwargs)