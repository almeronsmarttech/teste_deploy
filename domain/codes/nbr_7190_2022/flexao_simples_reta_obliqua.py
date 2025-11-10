
def flexao(madeira, secao_transversal, acoes):
    # esbeltez lambda

    sigma_Md = acoes.MSdx / secao_transversal.Wx

    percentual =  sigma_Md/ madeira.fc0d

    return sigma_Md, madeira.fc0d, percentual
