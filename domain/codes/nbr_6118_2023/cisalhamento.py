import numpy as np

def dimensionar_cisalhamento_secao_retangular(bw, h, cortante, estrutura) -> float:
    cortante = abs(cortante)
    d = h - 5
    mi = (estrutura.gama_F * cortante * 100) / (bw * d * d * 0.85 * estrutura.concreto.fcd)
    print(
        f"gama_F: {estrutura.gama_F}\tmomento: {cortante:.2f} kN.m\tb: {bw}\td: {d:.2f} cm\tfcd: {estrutura.concreto.fcd:.4f} kN/cm2")
    xsi = (1 - np.sqrt(1 - 2 * mi)) / 0.8
    print(f"mi: {mi:.4f}\txsi: {xsi:.4f}")
    return 0.8 * xsi * bw * d * 0.85 * estrutura.concreto.fcd / estrutura.aco.fyd