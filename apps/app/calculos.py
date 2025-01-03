import math

def Tensao(esl, fyd, es):
    # Calcula a tensão no aço
    # es = módulo de elasticidade do aço em kN/cm2
    # esl = deformação de entrada
    # fyd = tensão de escoamento de cálculo em kN/cm2
    # tsl = tensão de saída em kN/cm2

    # Trabalhando com deformação positiva
    ess = math.fabs(esl)
    eyd = fyd / es
    if ess < eyd:
        tsl = es * ess
    else:
        tsl = fyd
    # Trocando o sinal se necessário
    if esl < 0:
        tsl = -tsl
    return tsl

def FNSR(fck, fyk, es,gamac,gamas,gamaf,bduct,b,h,d, amk):
    dl = h - d
    if fck <= 50:
        alamb = 0.8
        alfac = 0.85
        eu = 3.5
        qlim = 0.8 * bduct - 0.35
    elif fck > 50 and fck <= 90:
        alamb = 0.8 - (fck - 50) / 400
        alfac = 0.85 * (1 - (fck - 50) / 200)
        a = (90 - fck) / 100
        eu = 2.6 + 0.35 * math.pow(a, 4)
        qlim = 0.8 * bduct - 0.45
    # Conversão de unidades: transformando para kN e cm
    amk *= 100
    fck /= 10
    fyk /= 10
    es *= 100
    # Resistências de cálculo
    fcd = fck / gamac
    tcd = alfac * fcd
    fyd = fyk / gamas
    amd = gamaf * amk
    # Parâmetro geométrico
    delta = dl / d
    # Momento limite
    amilim = alamb * qlim * (1 - 0.5 * alamb * qlim)
    # Momento reduzido solicitante
    ami = amd / (b * d * d * tcd)

    if ami <= amilim:
        print("Armadra simples.")
        qsi = (1 - math.sqrt(1 - 2 * ami)) / alamb
        aas = alamb * qsi * b * d * tcd / fyd
        asl = 0
    else:
        print("Armadra dupla.")
        # Evitando armadura dupla no domínio 2
        qsia = eu / (eu + 10)
        if qlim < qsia:
            # Está resultando armadura dupla no domínio 2.
            # Colocar mensagem para o usuário aumentar as dimensões da seção transversal e parar o processamento
            print("Resultou armadura dupla no domínio 2. Aumente as dimensões da seção transversal.")
        # Eliminando o caso em que qlim<delta
        # Se isto ocorrer, a armadura de compressão estará tracionada
        if qlim <= delta:
            print("Aumente as dimensões da seção transversal.")
        # Deformação da armadura de compressão
        esl = eu * (qlim - delta) / qlim
        esl = esl / 1000
        # Tensão na armadura de compressão
        tsl = Tensao(esl, fyd, es)
        asl = (ami - amilim) * b * d * tcd / ((1 - delta) * tsl)
        aas = (alamb * qlim + (ami - amilim) / (1 - delta)) * b * d * tcd / fyd

    # Armadura mínima
    a = 2.0 / 3.0
    fck *= 10
    fyd *= 10

    if fck <= 50:
        romin = 0.078 * math.pow(fck, a) / fyd
    else:
        romin = 0.5512 * math.log(1 + 0.11 * fck) / fyd
    if romin < 0.0015:
        romin = 0.0015

    asmin = romin * b * h
    print(f"Asmin: {round(asmin, 2)} cm2")
    if aas < asmin:
        aas = asmin
    # Convertendo a saída para duas casas decimais
    saida1 = round(aas, 2)
    saida2 = round(asl, 2)
    # MOSTRAR O RESULTADO
    # Área da armadura tracionada: aas
    print("\nÁrea da armadura tracionada")
    print(f"As adotada: {saida1} cm2")
    # Área da armadura comprimida: asl
    print("\nÁrea da armadura comprimida")
    print(f"As' adotada: {saida2} cm2")
    return round(asmin,2), round(aas,2), round(asl,2)