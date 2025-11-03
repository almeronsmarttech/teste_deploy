
def tracao(madeira, secao_transversal, acoes, num_furo =0, bitola = 0):
    # esbeltez lambda

    if secao_transversal.lambda_x >= 140 or secao_transversal.lambda_y >= 140:
        print(
            f"lambda = {max(secao_transversal.lambda_x, secao_transversal.lambda_y)}. O lambda deve ser menor que 140.\nReveja as dimensões da peça ou o comprimento do elemento.")


    sigma_Ncd = acoes.NSd / secao_transversal.Aw

    if madeira.ft0d < sigma_Ncd:
        print("Tensão resistente menor que a atuante. Rever dimensões, altura ou madeira.")
        exit()

    sigma_Mxcd = (acoes.MSdx * secao_transversal.hx / 2) / secao_transversal.Ix
    sigma_Mycd = (acoes.MSdy * secao_transversal.hy / 2) / secao_transversal.Iy

    tensao_sigma = (sigma_Ncd / madeira.ft0d) + (sigma_Mxcd / madeira.fc0d) + (sigma_Mycd / madeira.fc0d)

    print(
        f"Equação Simplificada Solicitações Compostas\nsigma Ncd = {round(sigma_Ncd, 2)} kN/cm2\tsigma_Mxcd = {round(sigma_Mxcd, 2)} kNcm\tsigma_Mycd = {round(sigma_Mycd, 2)} kNcm")

    print(f"Tensão Sigma Composta: {tensao_sigma}")
    if tensao_sigma < 1:
        print("OK! Tensão resistente MAIOR que a atuante!")
    else:
        print("Tensão resistente MENOR que a atuante! REVER!")

    return tensao_sigma
