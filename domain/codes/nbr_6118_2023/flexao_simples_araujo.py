import numpy as np

# def dimensionar_flexao_secao_retangular(bw, h, momento, estrutura) -> float:
#     momento = abs(momento)
#     d = h - 5
#     if estrutura.concreto.fck <= 35:
#         xsi_lim = 0.45
#         mi_lim = 0.2952
#     else:
#         xsi_lim =0.35
#         mi_lim = 0.2408
#     mi = (estrutura.gama_F * momento * 100) / (bw * d * d * 0.85 * estrutura.concreto.fcd)
#     print(
#         f"gama_F: {estrutura.gama_F}\tmomento: {momento:.2f} kN.m\tb: {bw}\td: {d:.2f} cm\tfcd: {estrutura.concreto.fcd:.4f} kN/cm2")
#     xsi = (1 - np.sqrt(1 - 2 * mi)) / 0.8
#     print(f"mi: {mi:.4f}\txsi: {xsi:.4f}")
#     #if mi < mi_lim and xsi < xsi_lim:
#         #return "Armadura mínima."
#     #    return 0.8 * xsi * bw * d * 0.85 * estrutura.concreto.fcd / estrutura.aco.fyd
#
#     return 0.8 * xsi * bw * d * 0.85 * estrutura.concreto.fcd / estrutura.aco.fyd

def dimensionar_flexao_secao_retangular(viga, momento, estrutura):
    as_trac, as_comp = 0,0
    momento = abs(momento)
    #xsi_lim = estrutura.concreto._beta_lim
    if estrutura.concreto.fck <= 50:
        xsi_lim = 0.45
        mi_lim = 0.2952
    else:
        xsi_lim = 0.35
        mi_lim = 0.2408

    fck = estrutura.concreto.fck
    fcd = estrutura.concreto.fcd
    fyd = estrutura.aco.fyd
    bw = viga._bw
    d = viga._d
    sigma_cd = estrutura.concreto._alfa * fcd
    mi = (estrutura.gama_F * momento * 100) / (bw * d * d * sigma_cd)
    print(f"gama_F: {estrutura.gama_F}\tmomento: {momento:.2f} kN.m\tb: {bw}\td: {d:.2f} cm\tfck: {fck:.4f}\tfcd: {fcd:.4f}\talfa: {estrutura.concreto._alfa:.4f}\tlambda: {estrutura.concreto._lambda:.4f}")
    xsi = (1 - np.sqrt(1 - 2 * mi)) / estrutura.concreto._lambda
    print(f"mi: {mi:.4f}\txsi: {xsi:.4f}")

    as_trac = estrutura.concreto._alfa * xsi * bw * d * estrutura.concreto._alfa * fcd / fyd

    if mi > mi_lim:
        # Armadura Dupla
        if fck <= 50:
            eu = 3.5/1000
        else:
            eu = 2.6 + 35*((90-fck)/100)**4
        delta = viga._dl / viga._d

        esl = eu * ((xsi_lim - delta)/xsi_lim)

        sigma_sdl = estrutura.aco._es * esl

        as_comp = ((mi-mi_lim)*bw*d*sigma_cd)/((1-delta)*sigma_sdl)
        as_trac = (estrutura.concreto._lambda*xsi_lim+((mi-mi_lim)/(1-delta)))*(bw*d*sigma_cd/fyd)
        #return as_trac, as_comp

    #if xsi > xsi_lim:
    #    return "Aumentar as dimensões da viga"

    return as_trac, as_comp


def dimensionar_flexao_secao_retangular_temp1(bw, d, momento, estrutura):
    momento = abs(momento)
    if estrutura.concreto.fck <= 35:
        xsi_lim = 0.45
        mi_lim = 0.2952
    else:
        xsi_lim = 0.35
        mi_lim = 0.2408

    fcd = estrutura.concreto.fcd
    fyd = estrutura.aco.fyd

    mi = (estrutura.gama_F * momento * 100) / (bw * d * d * 0.85 * fcd)
    print(f"gama_F: {estrutura.gama_F}\tmomento: {momento:.2f} kN.m\tb: {bw}\td: {d:.2f} cm\tfcd: {fcd:.4f}")

    try:
        xsi = (1 - np.sqrt(1 - 2 * mi)) / 0.8
    except ValueError:
        return "Momento excessivo para a seção — reveja as dimensões ou materiais."

    print(f"mi: {mi:.4f}\txsi: {xsi:.4f}")

    if mi > mi_lim:
        return "Armadura Dupla"
    if xsi > xsi_lim:
        return "Aumentar as dimensões da viga"

    return 0.8 * xsi * bw * d * 0.85 * fcd / fyd


def dimensionar_flexao_secao_retangular_temp(bw, h, momento, estrutura) -> float:
    momento = abs(momento)
    d = h - 5
    bduct = 1
    if estrutura.concreto.fck <= 50:
        alamb = 0.8
        alfac = 0.85
        eu = 3.5
        qlim = 0.8 * bduct - 0.35
    elif estrutura.concreto.fck > 50 and estrutura.concreto.fck < 90:
        alamb = 0.8 - (estrutura.concreto.fck - 50) / 400
        alfac = 0.85 * (1 - (estrutura.concreto.fck - 50) / 200)
        a = (90 - estrutura.concreto.fck) / 100
        eu = 2.6 + 0.35 * np.pow(a, 4)
        qlim = 0.8 * bduct - 0.45
    mi = (estrutura.gama_F * momento * 100) / (bw * d * d * 0.85 * estrutura.concreto.fcd)
    milim = alamb * qlim * (1 - 0.5 * alamb * qlim)

    print(
        f"gama_F: {estrutura.gama_F}\tmomento: {momento:.2f} kN.m\tb: {bw}\td: {d:.2f} cm\tfcd: {estrutura.concreto.fcd:.4f} kN/cm2")
    xsi = (1 - np.sqrt(1 - 2 * mi)) / 0.8
    print(f"mi: {mi:.4f}\txsi: {xsi:.4f}")

    if mi <= milim:
        print("Armadra simples.")
        qsi = (1 - np.sqrt(1 - 2 * mi)) / alamb
        aas = alamb * qsi * bw * d * tcd / estrutura.aco.fyd
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
        tsl = Tensao(esl)
        asl = (mi - milim) * bw * d * tcd / ((1 - delta) * tsl)
        aas = (alamb * qlim + (mi - milim) / (1 - delta)) * bw * d * tcd / estrutura.aco.fyd

    # Armadura mínima
    a = 2.0 / 3.0
    estrutura.concreto.fck *= 10
    estrutura.aco.fyd *= 10

    if estrutura.concreto.fck <= 50:
        romin = 0.078 * np.pow(estrutura.concreto.fck, a) / estrutura.aco.fyd
    else:
        romin = 0.5512 * np.log(1 + 0.11 * estrutura.concreto.fck) / estrutura.aco.fyd
    if romin < 0.0015:
        romin = 0.0015

    asmin = romin * bw * h
    print(f"\nAsmin: {round(asmin, 2)} cm2")
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

    return 0.8 * xsi * bw * d * 0.85 * estrutura.concreto.fcd / estrutura.aco.fyd