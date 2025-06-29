# def bhaskara(a, b, c):
#     delta = b ** 2 - 4 * a * c
#     if delta < 0:
#         return None  # Ou uma mensagem: "Não existem raízes reais"
#
#     raiz_delta = delta ** 0.5
#     x1 = (-b + raiz_delta) / (2 * a)
#     x2 = (-b - raiz_delta) / (2 * a)
#     return x1, x2


def bhaskara(a, b, c):
    delta = b ** 2 - 4 * a * c
    if delta < 0:
        return None  # Ou uma mensagem: "Não existem raízes reais"

    raiz_delta = delta ** 0.5
    x1 = (-b + raiz_delta) / (2 * a)
    x2 = (-b - raiz_delta) / (2 * a)
    return x1, x2

def mais_proximo(referencia, op1, op2):
    return op1 if abs(referencia - op1) < abs(referencia - op2) else op2