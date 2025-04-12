from django.middleware.csrf import get_token


class CsrfMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        csrf_token = get_token(request)

        print(f"🔹 [Django] Middleware - CSRF Token enviado na resposta: {csrf_token}")  # Log no console

        response["X-CSRFToken"] = csrf_token  # Adiciona o CSRF Token no cabeçalho da resposta
        return response
