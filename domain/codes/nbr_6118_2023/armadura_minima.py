def ro_min(fck: int) -> float:
    """
    Retorna ρmin (armadura mínima relativa) conforme a NBR 6118:2023.
    """
    match int(fck):
        case 20 | 25 | 30:
            return 0.0015
        case 35:
            return 0.00164
        case 40:
            return 0.00179
        case 45:
            return 0.00194
        case 50:
            return 0.00208
        case 55:
            return 0.00211
        case 60:
            return 0.00219
        case 65:
            return 0.00226
        case 70:
            return 0.00233
        case 75:
            return 0.00239
        case 80:
            return 0.00245
        case 85:
            return 0.00251
        case 90:
            return 0.00256
        case _:
            raise ValueError(f"fck {fck} fora da faixa válida para a NBR 6118.")


def row_min(fck: int) -> float:
    """ Retorna ρmin (armadura mínima relativa) conforme a NBR 6118:2023 """

#     'Resistência média à tração do concreto
#     '
#     If(fck <= 50)
#     Then
#     a = 2 / 3
#     fctm = 0.3 * (fck ^ a)
#     Else
#     fctm = 2.12 * Math.Log(1 + 0.11 * fck)
#     End
#     If
#     '
#     'Taxa mínima de armadura (ver equação (1.4.5) do Volume 4)
#     rowmin = 0.2 * fctm / fykmax
#
# from domain.materials.concreto import Concreto
#     lista = []
#     for i in range(20, 95, 5):
#         lista.append(Concreto(fck=i))
#
#     tab_rowmin = []
#
#     for i in lista:
#         tab_rowmin.append(0.2 * i._fctk_m / aco.fywd)

    # 20 0.10167926936247465
    # 25 0.11798834032069208
    # 30 0.1332375350755769
    # 35 0.14765827231798095
    # 40 0.16140577914935017
    # 45 0.17459056171746207
    # 50 0.1872948155450485
    # 55 0.1904592531926938
    # 60 0.19778501707594368
    # 65 0.20459870826569027
    # 70 0.2109672614624157
    # 75 0.21694528874465308
    # 80 0.2225779302511749
    # 85 0.22790292540225357
    # 90 0.23295214720620677
    match int(fck):
        case 20:
            return 0.0009
            #return 0.0010167926936247465
        case 25:
            return 0.0010
            #return 0.0011798834032069208
        case 30:
            #return 0.0012
            return 0.0013323753507557688
        case 35:
            #return 0.0013
            return 0.0014765827231798096
        case 40:
            #return 0.0014
            return 0.0016140577914935017
        case 45:
            #return 0.0015
            return 0.0017459056171746207
        case 50:
            #return 0.0016
            return 0.001872948155450485
        case 55:
            return 0.001904592531926938
        case 60:
            return 0.0019778501707594367
        case 65:
            return 0.0020459870826569026
        case 70:
            return 0.002109672614624157
        case 75:
            return 0.002169452887446531
        case 80:
            return 0.002225779302511749
        case 85:
            return 0.0022790292540225358
        case 90:
            return 0.0023295214720620676
        case _:
            raise ValueError(f"fck {fck} fora da faixa válida para a NBR 6118.")
