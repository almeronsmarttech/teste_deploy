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
    """
    Retorna ρmin (armadura mínima relativa) conforme a NBR 6118:2023.
    """
    match int(fck):
        case 20:
            return 0.0009
        case 25:
            return 0.0010
        case 30:
            return 0.0012
        case 35:
            return 0.0013
        case 40:
            return 0.0014
        case 45:
            return 0.0015
        case 50:
            return 0.0016

        case _:
            raise ValueError(f"fck {fck} fora da faixa válida para a NBR 6118.")
