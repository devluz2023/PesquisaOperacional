"""
otimizacao_navio_carga.py
-------------------------
Otimização do transporte de carne de boi e grãos em compartimento de navio.
Resolução gráfica da região viável, restrições e ponto ótimo via Matplotlib.
"""

import matplotlib.pyplot as plt
import numpy as np


def plotar_otimizacao_navio():
    # Definição do grid de valores para x1 (Carne em milhares de kg)
    x1_max = 120
    x1_vals = np.linspace(0, x1_max, 500)

    # Equações das fronteiras isolando x2 (Grãos em milhares de kg)
    # 1. Peso: x1 + x2 <= 160 => x2 = 160 - x1
    r_peso = 160.0 - x1_vals

    # 2. Volume: 0.2*x1 + 0.4*x2 <= 70 => x2 = (70 - 0.2*x1) / 0.4
    r_volume = (70.0 - 0.2 * x1_vals) / 0.4

    # 3. Limite de Grão: x2 <= 100
    r_grao = np.full_like(x1_vals, 100.0)

    fig, ax = plt.subplots(figsize=(10, 7))

    # Curvas de restrição
    ax.plot(
        x1_vals,
        r_peso,
        label=r"Peso: $x_1 + x_2 \leq 160$ (Ativa)",
        color="royalblue",
        linewidth=2,
    )
    ax.plot(
        x1_vals,
        r_volume,
        label=r"Volume: $0{,}2x_1 + 0{,}4x_2 \leq 70$ (Folga: $23.000\mathrm{m^3}$)",
        color="darkorange",
        linestyle="--",
        linewidth=2,
    )
    ax.axhline(
        100,
        color="purple",
        linestyle="-.",
        linewidth=1.8,
        label=r"Oferta Grãos: $x_2 \leq 100$ (Folga: $25.000\mathrm{kg}$)",
    )
    ax.axvline(
        85,
        color="forestgreen",
        linewidth=2,
        label=r"Oferta Carne: $x_1 \leq 85$ (Ativa)",
    )

    # Vértices da região viável no primeiro quadrante (em milhares de kg)
    # V1(0, 0), V2(0, 100), V3(60, 100), V4(85, 75), V5(85, 0)
    # Note que para x2=100 e peso x1+x2=160, a interseção é x1=60.
    pontos_poligono = np.array(
        [[0, 0], [0, 100], [60, 100], [85, 75], [85, 0]]
    )

    poligono = plt.Polygon(
        pontos_poligono,
        closed=True,
        color="mediumseagreen",
        alpha=0.25,
        label="Região Viável",
    )
    ax.add_patch(poligono)

    # Ponto Ótimo: (85, 75)
    x1_opt, x2_opt = 85.0, 75.0
    lucro_opt = 0.35 * (x1_opt * 1000) + 0.12 * (x2_opt * 1000)

    # Isocurva da Função Objetivo no Ponto Ótimo:
    # 0.35*x1 + 0.12*x2 = Z => x2 = (Z - 0.35*x1) / 0.12
    # Z em milhares de R$ = 38.75
    z_milhares = lucro_opt / 1000
    r_obj = (z_milhares - 0.35 * x1_vals) / 0.12
    ax.plot(
        x1_vals,
        r_obj,
        color="crimson",
        linewidth=2.2,
        linestyle="-",
        label=rf"F.O. Ótima ($Z^* = \mathrm{{R\$}}\,{lucro_opt:,.2f}$)",
    )

    # Demais vértices
    vertices = {
        r"$V_1(0; 0)$": (0, 0),
        r"$V_2(0; 100)$": (0, 100),
        r"$V_3(60; 100)$": (60, 100),
        r"$V_5(85; 0)$": (85, 0),
    }

    for rotulo, (vx, vy) in vertices.items():
        z_v = (0.35 * vx + 0.12 * vy) * 1000
        ax.plot(vx, vy, "ko", markersize=5)
        ax.annotate(
            f"{rotulo}\n[R$ {z_v:,.0f}]",
            (vx, vy),
            textcoords="offset points",
            xytext=(7, 5),
            fontsize=8.5,
        )

    # Destaque do Ponto Ótimo
    ax.plot(
        x1_opt,
        x2_opt,
        "ro",
        markersize=9,
        label=rf"Ótimo $V_4({x1_opt:.0f};\, {x2_opt:.0f})$",
    )
    ax.annotate(
        f"$V_4(85; 75)$ — ÓTIMO\nCarne: 85.000 kg\nGrão: 75.000 kg\nLucro: R$ {lucro_opt:,.2f}",
        (x1_opt, x2_opt),
        textcoords="offset points",
        xytext=(15, 10),
        fontsize=9.5,
        fontweight="bold",
        color="darkred",
        bbox=dict(
            boxstyle="round,pad=0.4", fc="mistyrose", ec="crimson", alpha=0.9
        ),
        arrowprops=dict(arrowstyle="->", color="darkred", lw=1.5),
    )

    ax.set_xlim(-5, 115)
    ax.set_ylim(-5, 140)
    ax.set_xlabel(r"Carne de Boi ($x_1$) [em milhares de kg]", fontsize=11)
    ax.set_ylabel(r"Grãos ($x_2$) [em milhares de kg]", fontsize=11)
    ax.set_title(
        r"Otimização da Carga do Navio — Região Viável e Ponto Ótimo",
        fontsize=13,
        pad=12,
    )
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.legend(loc="upper right", framealpha=0.92, fontsize=8.5)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    plotar_otimizacao_navio()