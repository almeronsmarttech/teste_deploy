from math import pi, pow
def flambagem_lateral(L1, madeira, b, h, acoes):
    # esbeltez lambda

    primeira_parte = L1 / b
    betaE = 4
    betaM1 = 4/pi
    betaM2 = betaE/acoes.gamaF
    betaM3 = pow(h/b,3/2)
    betaM4 = ((h/b)-0.63)**0.5

    betaM = betaM1 * betaM2 * (betaM3 / betaM4)


    segunda_parte = madeira.E0ef / (betaM * madeira.fmd)
    # resistência
    print(f"betaM: {betaM}\tL1/b: {primeira_parte}\tsegunda parte: {segunda_parte}")
    parte1 = primeira_parte
    parte2 = segunda_parte
    return parte1, parte2