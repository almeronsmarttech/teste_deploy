def desenhar_svg_pilar(hx, hy, num_barras_x, num_barras_y, cor_fundo="#FFFFFF", cor_barras="black"):
    d_linha = 5  # cm
    margem = 30
    escala = 5
    largura_svg = int(hx * escala + 2 * margem)
    altura_svg = int(hy * escala + 2 * margem)

    x0 = margem
    y0 = margem
    x1 = x0 + hx * escala
    y1 = y0 + hy * escala

    barras = []

    espaco_x = (hx - 2 * d_linha) / (num_barras_x - 1) if num_barras_x > 1 else 0
    for i in range(num_barras_x):
        x = x0 + (d_linha + i * espaco_x) * escala
        barras.append((x, y0 + d_linha * escala))
        barras.append((x, y1 - d_linha * escala))

    espaco_y = (hy - 2 * d_linha) / (num_barras_y - 1) if num_barras_y > 1 else 0
    for j in range(1, num_barras_y - 1):
        y = y0 + (d_linha + j * espaco_y) * escala
        barras.append((x0 + d_linha * escala, y))
        barras.append((x1 - d_linha * escala, y))

    svg = f"""
    <svg width="{largura_svg}" height="{altura_svg}" xmlns="http://www.w3.org/2000/svg" font-family="Arial" font-size="12">
        <defs>
            <marker id="seta" viewBox="0 0 10 10" refX="5" refY="5"
                markerWidth="6" markerHeight="6"
                orient="auto-start-reverse">
                <path d="M 0 0 L 10 5 L 0 10 z" fill="black" />
            </marker>
        </defs>

        <rect x="{x0}" y="{y0}" width="{hx*escala}" height="{hy*escala}"
              fill="{cor_fundo}" stroke="black" stroke-width="2" />

        {''.join(f'<circle cx="{x}" cy="{y}" r="5" fill="{cor_barras}" />' for x, y in barras)}

        <line x1="{x0}" y1="{y1 + 20}" x2="{x1}" y2="{y1 + 20}" stroke="black" marker-start="url(#seta)" marker-end="url(#seta)" />
        <line x1="{x0}" y1="{y1}" x2="{x0}" y2="{y1 + 30}" stroke="black" />
        <line x1="{x1}" y1="{y1}" x2="{x1}" y2="{y1 + 30}" stroke="black" />
        <text x="{(x0 + x1)/2}" y="{y1 + 18}" text-anchor="middle">hx = {hx:.0f} cm</text>

        <line x1="{x1 + 20}" y1="{y0}" x2="{x1 + 20}" y2="{y1}" stroke="black" marker-start="url(#seta)" marker-end="url(#seta)" />
        <line x1="{x1}" y1="{y0}" x2="{x1 + 30}" y2="{y0}" stroke="black" />
        <line x1="{x1}" y1="{y1}" x2="{x1 + 30}" y2="{y1}" stroke="black" />
        <text x="{x1 + 22}" y="{(y0 + y1)/2}" text-anchor="start" dominant-baseline="middle" transform="rotate(90,{x1 + 22},{(y0 + y1)/2})">hy = {hy:.0f} cm</text>
    </svg>
    """
    return svg


def desenhar_svg_resultado(hx, hy, num_barras_x, num_barras_y, e_x=0, e_y=0, desenhar_carga=True):
    d_linha = 5  # cm
    margem = 30
    escala = 5  # 1 cm = 5 px
    largura_svg = int(hx * escala + 2 * margem)
    altura_svg = int(hy * escala + 2 * margem)

    x0 = margem
    y0 = margem
    x1 = x0 + hx * escala
    y1 = y0 + hy * escala

    x_centro = x0 + (hx / 2) * escala
    y_centro = y0 + (hy / 2) * escala

    barras = []

    espaco_x = (hx - 2 * d_linha) / (num_barras_x - 1) if num_barras_x > 1 else 0
    for i in range(num_barras_x):
        x = x0 + (d_linha + i * espaco_x) * escala
        barras.append((x, y0 + d_linha * escala))  # topo
        barras.append((x, y1 - d_linha * escala))  # base

    espaco_y = (hy - 2 * d_linha) / (num_barras_y - 1) if num_barras_y > 1 else 0
    for j in range(1, num_barras_y - 1):
        y = y0 + (d_linha + j * espaco_y) * escala
        barras.append((x0 + d_linha * escala, y))  # esquerda
        barras.append((x1 - d_linha * escala, y))  # direita

    svg = f"""
    <svg width="{largura_svg}" height="{altura_svg}" xmlns="http://www.w3.org/2000/svg" font-family="Arial" font-size="12">
        <rect x="{x0}" y="{y0}" width="{hx * escala}" height="{hy * escala}" fill="#BFDBFE" stroke="black" stroke-width="2" />
        {''.join(f'<circle cx="{x}" cy="{y}" r="5" fill="red" />' for x, y in barras)}
    """

    if desenhar_carga:
        cx = x_centro + e_x * escala
        cy = y_centro - e_y * escala  # ey positivo sobe

        # Posição de Nd ajustada conforme os sinais
        nd_dx = 8 if e_x >= 0 else -24
        nd_dy = -8 if e_y >= 0 else 14

        # Círculo da carga e texto Nd reposicionado
        svg += f'''
            <circle cx="{cx}" cy="{cy}" r="6" fill="orange" stroke="black" stroke-width="2" />
            <text x="{cx + nd_dx}" y="{cy + nd_dy}" fill="black" font-size="14" font-weight="bold">Nd</text>
        '''

        # Cota horizontal (e_x)
        svg += f'''
            <line x1="{x_centro}" y1="{cy}" x2="{cx}" y2="{cy}" stroke="black" stroke-dasharray="4" />
            <text x="{(cx + x_centro)/2}" y="{cy - (8 if e_x >= 0 else -16)}" fill="black" text-anchor="middle" font-size="11">{round(e_x, 1)} cm</text>
            <line x1="{cx}" y1="{cy - 5}" x2="{cx}" y2="{cy + 5}" stroke="black" />
            <line x1="{x_centro}" y1="{cy - 5}" x2="{x_centro}" y2="{cy + 5}" stroke="black" />
        '''

        # Cota vertical (e_y)
        svg += f'''
            <line x1="{cx}" y1="{y_centro}" x2="{cx}" y2="{cy}" stroke="black" stroke-dasharray="4" />
            <text x="{cx + (10 if e_x >= 0 else -35)}" y="{(cy + y_centro)/2 + 4}" fill="black" font-size="11">{round(e_y, 1)} cm</text>
            <line x1="{cx - 5}" y1="{cy}" x2="{cx + 5}" y2="{cy}" stroke="black" />
            <line x1="{cx - 5}" y1="{y_centro}" x2="{cx + 5}" y2="{y_centro}" stroke="black" />
        '''

    svg += "</svg>"
    return svg

