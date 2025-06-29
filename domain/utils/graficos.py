# domain/utils/graficos.py
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os

def gerar_curva_resistente(pilar, Mx, My, nome_arquivo="curva_pilar.png"):
    sns.set_theme(style="whitegrid")
    alpha = 1.2

    Mrd_x = pilar.Mrd('x')
    Mrd_y = pilar.Mrd('y')
    Mrd_x_cm = Mrd_x * 100
    Mrd_y_cm = Mrd_y * 100

    theta = np.linspace(0, 2 * np.pi, 300)
    cos_a = np.abs(np.cos(theta)) ** (2 / alpha)
    sin_a = np.abs(np.sin(theta)) ** (2 / alpha)
    denom = (cos_a / Mrd_x_cm**(2 / alpha) + sin_a / Mrd_y_cm**(2 / alpha))
    raio = denom ** (-alpha / 2)

    Mx_curve = raio * np.cos(theta)
    My_curve = raio * np.sin(theta)

    fig, ax = plt.subplots(figsize=(7, 6))
    ax.fill(Mx_curve, My_curve, color='#14919B', alpha=0.25, label='Capacidade resistente')
    ax.plot(Mx_curve, My_curve, color='#0B6477', linewidth=1.8)

    ax.plot(Mx * 100, My * 100, 'o', color='#E67E22', label=f'Ação ({Mx:.2f}, {My:.2f}) kN·m')

    ax.set_xlabel('Mx (kN·cm)')
    ax.set_ylabel('My (kN·cm)')
    ax.set_title('Curva Resistente do Pilar')
    ax.legend()
    ax.grid(True)
    ax.axis('equal')

    caminho = f"static/graficos/{nome_arquivo}"
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    fig.tight_layout()
    fig.savefig(caminho)
    plt.close(fig)
    return "/" + caminho

def verificar_dentro(pilar, Mx, My):
    alpha = 1.2
    Mrd_x_cm = pilar.Mrd('x') * 100
    Mrd_y_cm = pilar.Mrd('y') * 100

    Mx_cm = Mx * 100
    My_cm = My * 100

    left = (abs(Mx_cm) / Mrd_x_cm) ** alpha + (abs(My_cm) / Mrd_y_cm) ** alpha
    return left <= 1.0
