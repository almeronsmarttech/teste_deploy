import numpy as np
import domain.codes.nbr_6118_2023.armadura_minima
from domain.materials.aco import Aco, Barra


def dimensionar_cisalhamento_secao_retangular(bw, h, Vk, estrutura) -> float:
    d = h - 5
    Vd = Vk * estrutura.gama_F
    print(f"Vd = {Vd:.2f}")
    tal_wd = Vd / (bw * d)
    alfa_v = 1 - estrutura.concreto.fck / 250
    print(f"alfa_v = {alfa_v:.2f}")
    tal_wu = 0.27 * alfa_v * estrutura.concreto.fcd
    print(f"tal_wu = {tal_wu:.2f}")

    if tal_wd <= tal_wu:
        print(
            f"Tal_wd = {tal_wd:.3f} kN/cm2 <= Tal_wu = {tal_wu:.3f} kN/cm2 -> Condição de esmagamento das bielas comprimidas atendido.")
        tal_c = 0.09 * (estrutura.concreto.fck  ** (2 / 3)) / 10
        print(f"Tal_c = {tal_c:.3f} kN/cm2")
        tal_d = 1.11 * (tal_wd - tal_c)
        print(f"Tal_d = {tal_d:.3f} kN/cm2")
        asw = 100 * bw * tal_d / estrutura.aco.fywd
    else:
        print(
            f"Tal_wd = {tal_wd:.3f} kN/cm2 > Tal_wu = {tal_wu:.3f} kN/cm2 -> Aumentar as dimensões da seção transversal.")
        asw = 0
    #print(f"Asw_min = {asw_min:.2f} cm2/m\tAsw_calc = {asw:.2f} cm2/m")
    print(f"Asw_calc = {asw}")
    return asw

    # def detalhamento_armaduras(self, As_necessario, cobertura = 1, tamanho = 1, numero_ramos = 2):
    #     bitolas_transversal = [
    #         Barra(Aco(fyk=600), diametro=5.0),
    #         Barra(Aco(fyk=500), diametro=6.3),
    #         Barra(Aco(fyk=500), diametro=8.0),
    #         Barra(Aco(fyk=500), diametro=10.0),
    #     ]
    #
    #     lista_resposta =[]
    #     for bitola in bitolas_transversal:
    #         num_barras = As_necessario/ (bitola.area_aco*numero_ramos)
    #         espacamento = int(np.floor(100 / num_barras))
    #
    #         if espacamento > 20:
    #             espacamento = 20
    #             #recalcula número de barras
    #             num_barras = 100 / 20
    #         if espacamento > 5:
    #             num_barras = int(np.ceil(num_barras * cobertura))
    #             print(
    #                 f"{num_barras} Φ de {bitola.diametro * 10:.1f} mm a cada {espacamento} cm.\tAs efetivo: {num_barras / cobertura * bitola.area_aco:.2f} cm2/m.")
    #             lista_resposta.append(
    #                 f"Φ de {bitola.diametro * 10:.1f} mm a cada {espacamento} cm. (As efetivo: {num_barras / cobertura * bitola.area_aco:.2f} cm2/m) -  N = {num_barras}    L = {tamanho:.2f} m ")
    #
    #     return lista_resposta


def detalhamento_armaduras(self, As_necessario, cobertura = 1, tamanho = 1, numero_ramos = 2):
    bitolas_transversal = [
        Barra(Aco(fyk=600), diametro=5.0),
        Barra(Aco(fyk=500), diametro=6.3),
        Barra(Aco(fyk=500), diametro=8.0),
        Barra(Aco(fyk=500), diametro=10.0),
    ]

    lista_resposta =[]
    for bitola in bitolas_transversal:
        num_barras = As_necessario/ (bitola.area_aco*numero_ramos)
        espacamento = int(np.floor(100 / num_barras))

        if espacamento > 20:
            espacamento = 20
            #recalcula número de barras
            num_barras = 100 / 20
        if espacamento > 5:
            num_barras = int(np.ceil(num_barras * cobertura))
            print(
                f"{num_barras} Φ de {bitola.diametro * 10:.1f} mm a cada {espacamento} cm.\tAs efetivo: {num_barras / cobertura * bitola.area_aco:.2f} cm2/m.")
            lista_resposta.append(
                f"Φ de {bitola.diametro * 10:.1f} mm a cada {espacamento} cm. (As efetivo: {num_barras / cobertura * bitola.area_aco:.2f} cm2/m) -  N = {num_barras}    L = {tamanho:.2f} m ")

    return lista_resposta

