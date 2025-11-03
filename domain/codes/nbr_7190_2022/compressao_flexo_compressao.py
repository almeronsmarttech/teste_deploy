
def compressao(madeira, secao_transversal, acoes):
    # esbeltez lambda

    if secao_transversal.lambda_x >= 140 or secao_transversal.lambda_y >= 140:
        print(
            f"lambda = {max(secao_transversal.lambda_x, secao_transversal.lambda_y)}. O lambda deve ser menor que 140.\nReveja as dimensões da peça ou o comprimento do elemento.")


    sigma_Ncd = acoes.NSd / secao_transversal.Aw

    if madeira.fc0d < sigma_Ncd:
        print("Tensão resistente menor que a atuante. Rever dimensões, altura ou madeira.")
        exit()

    sigma_Mxcd = (acoes.MSdx * secao_transversal.hx / 2) / secao_transversal.Ix
    sigma_Mycd = (acoes.MSdy * secao_transversal.hy / 2) / secao_transversal.Iy

    tensao_sigma = (sigma_Ncd / madeira.fc0d) + (sigma_Mxcd / madeira.fc0d) + (sigma_Mycd / madeira.fc0d)

    print(
        f"Equação Simplificada Solicitações Compostas\nsigma Ncd = {round(sigma_Ncd, 2)} kN/cm2\tsigma_Mxcd = {round(sigma_Mxcd, 2)} kNcm\tsigma_Mycd = {round(sigma_Mycd, 2)} kNcm")

    print(f"Tensão Sigma Composta: {tensao_sigma}")
    if tensao_sigma < 1:
        print("OK! Tensão resistente MAIOR que a atuante!")
    else:
        print("Tensão resistente MENOR que a atuante! REVER!")

    # ESTABILIDADE

    # Módulo de Elasticidade Característico
    E0_05 = 0.7 * madeira.Ec0med

    lambda_rel = (max(secao_transversal.lambda_x, secao_transversal.lambda_y) / 3.1415) * ((madeira.fc0k / E0_05)**0.5)

    print(f"E0,05 = {E0_05} kN/cm2\tlambda_rel = {round(lambda_rel, 2)}")

    beta_c = 0.2  # para madeira serrada retangular
    ver = 0
    if lambda_rel > 0.3:
        print("Tem que verificar a estabilidade")
        k = 0.5 * (1 + beta_c * (lambda_rel - 0.3) + (lambda_rel**2))

        # fator de instabilidade kc
        kc = 1 / (k + (((k**2) - (lambda_rel**2)))**0.5)
        print(f"k = {round(k, 2)}\tkc = {round(kc, 2)}")
        # Verificação da Estabilidade
        ver = sigma_Ncd / (kc * madeira.fc0d)  # (kc*fc0d) conhecido como resistência à flambagem
        print(f"Verificação:\nver = {round(ver, 2)}")
        if ver < 1:
            print("Verificação à flambagem passou!")
        else:
            print("A peça não passou a verificação de flambagem! Rever dimensões, material ou comprimentos livres.")



    return sigma_Ncd, lambda_rel, k, kc, ver
