import numpy as np

def dimensionar_flexao_secao_retangular(bw, h, momento, estrutura) -> float:
    momento = abs(momento)
    d = h - 5
    mi = (estrutura.gama_F * momento * 100) / (bw * d * d * 0.85 * estrutura.concreto.fcd)
    print(
        f"gama_F: {estrutura.gama_F}\tmomento: {momento:.2f} kN.m\tb: {bw}\td: {d:.2f} cm\tfcd: {estrutura.concreto.fcd:.4f} kN/cm2")
    xsi = (1 - np.sqrt(1 - 2 * mi)) / 0.8
    print(f"mi: {mi:.4f}\txsi: {xsi:.4f}")
    return 0.8 * xsi * bw * d * 0.85 * estrutura.concreto.fcd / estrutura.aco.fyd