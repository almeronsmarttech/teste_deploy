
def cisalhamento(madeira, secao_transversal, acoes):
    # esbeltez lambda

    tal_d = 1.5 * acoes.VSd / secao_transversal.Aw

    percentual = tal_d/ madeira.fv0d

    return tal_d, madeira.fv0d, percentual
