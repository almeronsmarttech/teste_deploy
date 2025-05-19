
from django.conf import settings
from django.shortcuts import redirect, render
import requests
import uuid
from .services import listar_metodos_pagamento
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def checkout(request):
    return render(request, 'subscriptions/checkout.html')

def success(request):
    return render(request, 'subscriptions/success.html')

def failure(request):
    return render(request, 'subscriptions/failure.html')

def checkout(request):
    context = {
        'public_key': settings.PUBLIC_KEY_MP
    }
    return render(request, 'subscriptions/checkout.html', context)

def test_payment_methods(request):
    metodos = listar_metodos_pagamento()
    return JsonResponse(metodos, safe=False)


@csrf_exempt
def process_payment(request):
    if request.method == "POST":
        payment_method = request.POST.get('payment_method')
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')

        # Para simulação simples de valor fixo (depois podemos tornar dinâmico)
        amount = 100.00

        if payment_method == 'pix':
            order_data = {
                "transaction_amount": amount,
                "payment_method_id": "pix",
                "description": "Pagamento de Teste",
                "payer": {
                    "email": email
                }
            }

            headers = {
                "Authorization": f"Bearer {settings.ACCESS_TOKEN_MP}",
                "Content-Type": "application/json",
                "X-Idempotency-Key": str(uuid.uuid4())
            }

            response = requests.post(
                "https://api.mercadopago.com/v1/payments",
                json=order_data,
                headers=headers
            )

            data = response.json()
            transaction_data = data.get("point_of_interaction", {}).get("transaction_data", {})

            return render(request, 'subscriptions/pix_payment.html', {
                'qr_code_base64': transaction_data.get('qr_code_base64'),
                'qr_code': transaction_data.get('qr_code'),
                'ticket_url': transaction_data.get('ticket_url')
            })


        elif payment_method == 'boleto':
            boleto_data = {
                "type": "online",
                "total_amount": amount,
                "external_reference": str(uuid.uuid4()),
                "processing_mode": "automatic",
                "transactions": [
                    {
                        "payments": [
                            {
                                "amount": amount,
                                "payment_method": {
                                    "id": "bolbradesco",
                                    "type": "ticket"
                                },
                                "payer": {
                                    "email": email
                                }
                            }
                        ]
                    }
                ]
            }

            headers = {
                "Authorization": f"Bearer {settings.ACCESS_TOKEN_MP}",
                "Content-Type": "application/json",
                "X-Idempotency-Key": str(uuid.uuid4())
            }

            response = requests.post(
                "https://api.mercadopago.com/v1/orders",
                json=boleto_data,
                headers=headers
            )

            if response.status_code in (200, 201):
                data = response.json()
                payment_info = data.get("transactions", [])[0]["payments"][0]["payment_method"]

                return render(request, 'subscriptions/boleto_payment.html', {
                    'ticket_url': payment_info.get('ticket_url')
                })
            else:
                return JsonResponse({
                    "error": "Erro ao criar boleto",
                    "status_code": response.status_code,
                    "details": response.json()
                })

        elif payment_method == 'card':
            # Simulação: você pode substituir com integração real depois
            return JsonResponse({'message': 'Pagamento com cartão enviado (simulação)'})

        else:
            return JsonResponse({'error': 'Método de pagamento inválido'})

    return JsonResponse({'error': 'Método não permitido'})