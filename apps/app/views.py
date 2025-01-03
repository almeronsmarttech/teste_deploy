from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView
from pyexpat.errors import messages
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime
from django.contrib.auth.decorators import login_required


from .calculos import FNSR

from .forms import Contato1Form, FlexaoNormalSimplesRetangularForm

# Create your views here.
class IndexView(TemplateView):
    ano_atual = datetime.now().year
    template_name = "app/index.html"

    def render_to_response(self, context, **response_kwargs):
        # Verifica se é uma requisição HTMX
        if self.request.headers.get('HX-Request'):
            # Renderiza apenas o conteúdo parcial
            return self.response_class(
                request=self.request,
                template=self.template_name,
                context=context,
                content_type='text/html',
            )
        # Caso contrário, renderiza o layout completo
        return super().render_to_response(context, **response_kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Verifica se o usuário está autenticado
        if self.request.user.is_authenticated:
            #context['message'] = f"Bem-vindo, {self.request.user.username}! Você está logado."
            context['logado'] = True
            if self.request.user.first_name and self.request.user.last_name == "" or self.request.user.first_name and self.request.user.last_name == None:
                context['nome_completo'] = "Usuário sem nome cadastrado."
            else:
                context['nome_completo'] = self.request.user.first_name.title() + " " + self.request.user.last_name.title()
        else:
            context['logado'] = False
            #context['message'] = "Você não está logado."
        context['ano_atual']=self.ano_atual
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
#@login_required
class CurvaView(TemplateView):
    template_name = "app/curva.html"

#@login_required
class FlexaoNormalSimplesRetangularView(FormView):
    template_name = 'app/flexao_normal_simples_retangular_form.html'
    form_class = FlexaoNormalSimplesRetangularForm

    def form_valid(self, form):
        instance = form.save(commit=False)
        dl = instance.dl
        ## gamac,gamas,gamaf,bduct,b,h,d, amk)
        aas = FNSR(form.cleaned_data['fck'],form.cleaned_data['fyk'],form.cleaned_data['es'],form.cleaned_data['gamac'],form.cleaned_data['gamas'],form.cleaned_data['gamaf'],form.cleaned_data['bduct'],form.cleaned_data['b'],form.cleaned_data['h'],form.cleaned_data['d'],form.cleaned_data['amk'])
        # Outros cálculos podem ser adicionados aqui

        return self.render_to_response(self.get_context_data(form=form, dl=dl, asmin= aas[0], aas= aas[1], asl=aas[2]))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
# fonte: https://blog.devgenius.io/django-and-htmx-a-powerful-duo-for-modern-web-development-be537fe280f1
def sobre(request):
    return render(request, 'app/sobre.html')

def load_content(request):
    return HttpResponse("<p>This content was loaded dynamically!</p>")

# Só está funcionando em funções, não em classes
@login_required
def contact_form(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        # Process the form (e.g., save to database, send email)
        return HttpResponse(f"Thanks, {name}! We've received your message.")
    return render(request, 'app/contact_form.html')