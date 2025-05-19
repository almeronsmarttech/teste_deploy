def cobrimento_nbr6118(tipo_elemento: str, caa: str) -> int:
    """
    Retorna o cobrimento nominal (mm) para concreto armado conforme NBR 6118:2023, Tabela 7.2.
    """
    tabela = {
        "laje":   {"I": 20, "II": 25, "III": 35, "IV": 45},
        "viga":   {"I": 25, "II": 30, "III": 40, "IV": 50},
        "pilar":  {"I": 25, "II": 30, "III": 40, "IV": 50},
        "solo":   {"I": 30, "II": 40, "III": 40, "IV": 50},
    }

    tipo = tipo_elemento.lower()
    classe = caa.upper()

    try:
        return tabela[tipo][classe]
    except KeyError:
        raise ValueError(f"Cobrimento não definido para tipo='{tipo_elemento}' e classe='{caa}'.")
