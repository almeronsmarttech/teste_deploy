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

def resolver_equacao_segundo_grau(A, B, C, condicao="menor_zero"):
    """
    Resolve Ax^2 + Bx + C e retorna valores de x que atendem a determinada condição:
    condicao:
        - "menor_zero": retorna os x onde f(x) < 0
        - "maior_zero": retorna os x onde f(x) > 0
    """
    delta = B**2 - 4 * A * C

    if delta < 0:
        return []  # Nenhuma solução real

    x1 = (-B + (delta)**0.5) / (2 * A)
    x2 = (-B - (delta)**0.5) / (2 * A)

    x_menor, x_maior = sorted([x1, x2])

    if condicao == "menor_zero":
        if A > 0:
            return [("entre", x_menor, x_maior)]
        else:
            return [("fora", x_menor, x_maior)]
    elif condicao == "maior_zero":
        if A > 0:
            return [("fora", x_menor, x_maior)]
        else:
            return [("entre", x_menor, x_maior)]
    else:
        raise ValueError("Condição inválida: use 'menor_zero' ou 'maior_zero'")