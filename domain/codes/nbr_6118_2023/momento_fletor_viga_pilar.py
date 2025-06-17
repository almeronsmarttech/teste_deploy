def momento_viga_pilar(l_inf, b_inf, h_inf, l_sup, b_sup, h_sup, l_viga, b_viga, h_viga, q_viga):
    r_inf = (b_inf * h_inf**3)/12 / (l_inf / 2)
    r_sup = (b_sup * h_sup**3)/12 / (l_sup / 2)
    r_vig = (b_viga * h_viga**3)/12 / l_viga
    r = (r_inf + r_sup)/(r_vig + r_inf + r_sup)
    Meng = q_viga * (l_viga/100) **2 / 12
    print(f"Método 1")
    print(f"Momento de Engastamento Perfeito da Viga = {Meng:.2f} kN.m")
    Mvig = r * Meng
    print(f"r inf = {r_inf:.2f}")
    print(f"r sup = {r_sup:.2f}")
    print(f"r viga = {r_vig:.2f}")
    print(f"Coeficiente = {r:.4f}")
    print(f"Momento na ligação:\n Viga = {Mvig:.2f} kN.m\tPilares = {Mvig/2:.2f} kN.m")
    return Mvig

def momento_viga_pilar_araujo_viga_continua(l_inf, b_inf, h_inf, l_sup, b_sup, h_sup, l_viga, b_viga, h_viga, q_viga):
    I_inf = b_inf * h_inf**3 / 12
    r_inf = (6*I_inf) / l_inf
    I_sup = b_sup * h_sup**3 / 12
    r_sup = (6* I_sup) / l_sup
    I_viga = (b_viga * h_viga**3)/12
    r_vig =  (4*I_viga)/ l_viga
    r = (r_inf + r_sup)/(r_vig + r_inf + r_sup)
    Meng = q_viga * (l_viga/100) **2 / 12
    print(f"Método Araújo Contínua")
    print(f"Momento de Engastamento Perfeito da Viga = {Meng:.2f} kN.m")

    Mvig = r * Meng

    print(f"r inf = {r_inf:.2f}")
    print(f"r sup = {r_sup:.2f}")
    print(f"r viga = {r_vig:.2f}")
    print(f"Coeficiente = {r:.4f}")
    print(f"Momento na ligação:\n Viga = {Mvig:.2f} kN.m\tPilares = {Mvig/2:.2f} kN.m")
    return Mvig

def momento_viga_pilar_araujo_viga_biapoiada(l_inf, b_inf, h_inf, l_sup, b_sup, h_sup, l_viga, b_viga, h_viga, q_viga):
    I_inf = b_inf * h_inf**3 / 12
    r_inf = (6*I_inf) / l_inf
    I_sup = b_sup * h_sup**3 / 12
    r_sup = (6* I_sup) / l_sup
    I_viga = (b_viga * h_viga**3)/12
    r_vig =  (3*I_viga)/ l_viga
    r = (r_inf + r_sup)/(r_vig + r_inf + r_sup)
    Meng = q_viga * (l_viga/100) **2 / 12
    print(f"Método Araújo Biapoiada")
    print(f"Momento de Engastamento Perfeito da Viga = {Meng:.2f} kN.m")
    Mvig = r * Meng
    print(f"r inf = {r_inf:.2f}")
    print(f"r sup = {r_sup:.2f}")
    print(f"r viga = {r_vig:.2f}")
    print(f"Coeficiente = {r:.4f}")
    print(f"Momento na ligação:\n Viga = {Mvig:.2f} kN.m\tPilares = {Mvig/2:.2f} kN.m")