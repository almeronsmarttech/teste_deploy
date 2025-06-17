import numpy as np
#from domain.elements.viga import VigaRetangular

"""
# Concreto - Rcc
sigma_cd = alfa_c * eta_c * fcd
Ac = bw * y
y = lambdaa * x
z = d - y / 2
z = d - 0.5 * lambdaa * x

Rcc = sigma_cd * Ac
# ou

Rcc = alfa_c * eta_c * fcd * bw * lambdaa * x

# Aço - Rst
Rst = sigma_sd * As
sigma_sd = fyd
# ou
Rst= fyd * As
"""
#def flexao_simples_retangular(viga: VigaRetangular, momento_calculo) -> list[float]:
def flexao_simples_retangular(viga, momento_calculo) -> list[float]:
    """ Função que calcula a área de aço de uma seção retangular sob flexão simples """
    as1, as2 = 0,0
    a = - 0.5 * viga._concreto._alfa * viga._concreto._eta * viga._concreto.fcd * viga._bw * viga._concreto._lambda * viga._concreto._lambda
    b = viga._concreto._alfa * viga._concreto._eta * viga._concreto.fcd * viga._bw * viga._concreto._lambda * viga._d
    c = - momento_calculo * 100
    x1, x2 = calcular_equacao_segundo_grau(a, b, c)
    linha_neutra_x = x2
    if linha_neutra_x / viga._d < viga._concreto._beta_lim:
        # armadura simples
        as1 = viga._concreto._alfa * viga._concreto._eta * viga._concreto.fcd * viga._bw * viga._concreto._lambda * linha_neutra_x / viga._aco.fyd
    else:
        # armadura dupla
        linha_neutra_x = viga._concreto._beta_lim * viga._d
        md1 = viga._concreto._alfa * viga._concreto._eta * viga._concreto.fcd * viga._bw * viga._concreto._lambda * linha_neutra_x * (
                    viga._d - 0.5 * viga._concreto._lambda * linha_neutra_x)
        as1 = viga._concreto._alfa * viga._concreto._eta * viga._concreto.fcd * viga._bw * viga._concreto._lambda * linha_neutra_x / viga._aco.fyd
        # momento resistido pela armadura de compressão
        md2 = momento_calculo - md1
        f2 = md2/(viga._h - 2 * viga._dl)
        as2 = f2/viga._aco.fyd
        as1 += as2

    as_min = calcular_as_min(viga)
    #print(f"as1: {max(as1, as_min)}, as2: {max(as2, as_min)}")
    print(f"as1: {as1:.2f}, as2: {as2:.2f}")

    if momento_calculo >= 0:

        return [max(as1,as_min), max(as2,as_min)]
    else:
        return [max(as2, as_min), max(as1, as_min)]


def calcular_equacao_segundo_grau(a: float, b: float, c: float) -> list[float]:
    """ Resolve a equação do segundo grau e retorna as raízes """
    x1, x2 = np.roots([a, b, c])
    print(f"x1 = {x1}\tx2 = {x2}")
    return [x1, x2]


fck_as_min = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90]
roh_min = [.15, .15, .15, .164, .179, .194, .208, .211, .219, .226, .233, .239, .245, .251, .256]


#def calcular_as_min(viga: VigaRetangular) -> float:
def calcular_as_min(viga) -> float:
    """ Função que retorna a área de aço mínimo conforme tabela do ítem 17.3 da NBR6118:2023"""
    as_min = 0
    for i, fck in enumerate(fck_as_min):
        if fck == viga._concreto.fck:
            as_min = viga._bw * viga._h * roh_min[i] / 100
    return as_min
