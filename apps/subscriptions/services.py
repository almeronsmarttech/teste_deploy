import mercadopago
from django.conf import settings

sdk = mercadopago.SDK(settings.ACCESS_TOKEN_MP)

def listar_metodos_pagamento():
    payment_methods_response = sdk.payment_methods().list_all()
    payment_methods = payment_methods_response["response"]
    return payment_methods
