from django.views.generic import TemplateView
import random
from django.views.generic import FormView, View
from django.conf import settings
from django.urls import reverse_lazy
from .forms import EmailLoginForm
from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.views.generic import FormView
from django.contrib.auth import login, logout
from django.contrib.auth import get_user_model
from django.http import HttpResponseBadRequest
from apps.loginapp.models import MyCustomUser
from django.shortcuts import redirect  # Importe o redirect no topo
from django.views.generic.edit import CreateView
from .forms import UserCreationForm

User = get_user_model()
attempts = {}  # Dicionário para armazenar tentativas temporárias

def header_partial(request):
    return render(request, "partials/header.html")

class UserCreationView(CreateView):
    form_class = UserCreationForm
    template_name = 'loginapp/user_creation_form.html'  # O template a ser usado
    success_url = reverse_lazy('home')  # Após a criação do usuário, redireciona para a home

class SignupPartialView(TemplateView):
    template_name = "loginapp/signup_partial.html"

class SendVerificationCodeView(View):
    def post(self, request, *args, **kwargs):
        email = request.POST.get("email")
        #print(f"📌 Recebido pedido de login para o e-mail: {email}")

        if not email:
            #print("🚨 Erro: Nenhum e-mail fornecido!")
            return HttpResponse("E-mail é obrigatório.", status=400)

        try:
            user = MyCustomUser.objects.get(email=email)

            # Gerar e salvar código de verificação
            verification_code = get_random_string(length=6, allowed_chars="0123456789")
            user.verification_code = verification_code
            user.save()

            # **Salvar o e-mail na sessão**
            request.session["pending_email"] = email
            request.session.modified = True  # Garante que a sessão seja salva
            #print(f"✅ E-mail salvo na sessão: {request.session['pending_email']}")

            # Enviar e-mail
            send_mail(
                subject="Seu Código de Verificação",
                message=f"Seu código de verificação é: {verification_code}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )

            #print("✅ Código de verificação enviado com sucesso!")

            # Retorna o template de verificação para inserir o código
            return render(request, "loginapp/verify_code_partial.html")

        except MyCustomUser.DoesNotExist:
            #print("🚨 Erro: Usuário não encontrado!")
            return HttpResponse("Usuário não encontrado.", status=400)

class VerifyCodeView(View):
    def post(self, request, *args, **kwargs):
        verification_code = request.POST.get("verification_code")
        email = request.session.get("pending_email")  # Obtém o e-mail salvo na sessão

        #print(f"📌 Tentativa de verificação de código!")
        #print(f"📌 Código recebido: {verification_code}")
        #print(f"📌 E-mail armazenado na sessão: {email}")

        if not email:
            #print("🚨 Erro: Nenhum e-mail encontrado na sessão!")
            return HttpResponseBadRequest("Sessão expirada. Refaça o login.")

        try:
            user = MyCustomUser.objects.get(email=email)

            #print(f"✅ Usuário encontrado: {user.email}")
            #print(f"✅ Código armazenado no usuário: {user.verification_code}")

            if user.verification_code == verification_code:
                #print("✅ Código correto! Autenticando usuário...")

                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)

                request.session.pop("pending_email", None)  # Remove o e-mail da sessão após login
                #print("✅ Usuário autenticado com sucesso!")

                return redirect("/")  # 🔄 Redireciona para a home após autenticação

            else:
                #print("🚨 Código inválido!")
                return HttpResponseBadRequest("Código inválido. Tente novamente.")

        except MyCustomUser.DoesNotExist:
            #print("🚨 Erro: Usuário não encontrado!")
            return HttpResponseBadRequest("Usuário não encontrado.")

class EmailLoginView(FormView):
    template_name = "loginapp/login_partial.html"
    form_class = EmailLoginForm
    success_url = reverse_lazy("verify_code")

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        # Aqui enviamos o código por e-mail (implemente a lógica real depois)
        return render(self.request, "loginapp/verify_email_partial.html", {"email": email})


class VerifyCodeView(View):
    def post(self, request, *args, **kwargs):
        verification_code = request.POST.get("verification_code")
        email = request.session.get("pending_email")

        if not email:
            return HttpResponse("Sessão expirada. Refaça o login.", status=400)

        try:
            user = User.objects.get(email=email)

            if user.verification_code == verification_code:
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
                request.session.pop("pending_email", None)  # Remove a sessão

                # 🔄 **HTMX redireciona para a home**
                response = HttpResponse()
                response["HX-Redirect"] = "/"
                return response

            else:
                return HttpResponse("Código inválido. Tente novamente.", status=400)

        except User.DoesNotExist:
            return HttpResponse("Usuário não encontrado.", status=400)


class ResendCodeView(View):
    """Reenvia o código de verificação"""
    def post(self, request, *args, **kwargs):
        email = request.session.get("pending_email")
        if not email:
            return redirect("account_login")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return redirect("account_login")

        # Gera um novo código e envia novamente
        verification_code = str(random.randint(100000, 999999))
        user.verification_code = verification_code
        user.save()

        send_mail(
            "Novo Código de Verificação",
            f"Seu novo código de verificação é: {verification_code}",
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        return render(request, "loginapp/verify_code_partial.html", {"email": email, "message": "Código reenviado com sucesso!"})


class FormPartialView(TemplateView):
    template_name = 'loginapp/login.html'
