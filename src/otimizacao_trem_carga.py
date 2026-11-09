"""
otimizacao_trem_carga.py
------------------------
Otimização do transporte de arroz e feijão em composição ferroviária.
Modelagem matemática e visualização gráfica do ponto ótimo e restrições.
"""

import matplotlib.pyplot as plt
import numpy as np


def plotar_otimizacao_trem():
    # Coordenadas em toneladas (1 t = 1.000 kg)
    # x1: Arroz total (t), x2: Feijão total (t)
    x1_vals = np.linspace(0, 110, 500)

    # 1. Capacidade total de peso imposta pela regra técnica:
    # Traseiro = 80t => Dianteiro <= 80 / 1.2 = 66.67t
    # x1 + x2 <= 80 + 66.67 = 146.67t
    peso_max_total = 80.0 + 80.0 / 1.2  # 146.6667 t
    r_peso = peso_max_total - x1_vals

    fig, ax = plt.subplots(figsize=(10, 7))

    # Curvas de restrição (usando chaves duplicadas para LaTeX dentro de f-strings)
    ax.plot(
        x1_vals,
        r_peso,
        label=r"Capacidade Máx. de Peso Efetiva ($x_1 + x_2 \leq 146{,}67\,$t)",
        color="royalblue",
        linewidth=2.2,
    )
    ax.axvline(
        85,
        color="forestgreen",
        linewidth=2,
        label=r"Disponibilidade de Arroz ($x_1 \leq 85\,$t)",
    )
    ax.axhline(
        100,
        color="purple",
        linestyle="--",
        linewidth=1.8,
        label=r"Disponibilidade de Feijão ($x_2 \leq 100\,$t)",
    )

    # Polígono da Região Viável no plano (Arroz Total x Feijão Total)
    pt_inter_feijao = peso_max_total - 100.0  # 46.6667 t
    x1_opt, x2_opt = 85.0, peso_max_total - 85.0  # (85.0, 61.6667)

    pontos_poligono = np.array(
        [[0, 0], [0, 100], [pt_inter_feijao, 100], [x1_opt, x2_opt], [85, 0]]
    )

    poligono = plt.Polygon(
        pontos_poligono,
        closed=True,
        color="mediumseagreen",
        alpha=0.25,
        label="Região Viável",
    )
    ax.add_patch(poligono)

    # Isocurva da Função-Objetivo Ótima (Z = R$ 37.150,00)
    z_opt = 0.35 * (x1_opt * 1000) + 0.12 * (x2_opt * 1000)
    r_z_opt = (z_opt - 350.0 * x1_vals) / 120.0
    ax.plot(
        x1_vals,
        r_z_opt,
        color="crimson",
        linewidth=2.4,
        label=rf"F.O. Ótima ($Z^* = \mathrm{{R\$}}\,{z_opt:,.2f}$)",
    )

    # Isocurva sub-ótima
    z_sub = 25000.0
    r_z_sub = (z_sub - 350.0 * x1_vals) / 120.0
    ax.plot(
        x1_vals,
        r_z_sub,
        color="crimson",
        linestyle=":",
        alpha=0.55,
        label=r"F.O. Sub-ótima ($Z = \mathrm{R\$}\,25.000$)",
    )

    # Ponto Ótimo Destacado (string crua simples, sem interpolação 'f')
    ax.plot(
        x1_opt,
        x2_opt,
        "ro",
        markersize=9,
        label=r"Ótimo ($x_1=85\,$t; $x_2=61{,}67\,$t)",
    )
    ax.annotate(
        f"PONTO ÓTIMO\n"
        f"Arroz Total: {x1_opt:.0f}.000 kg (100%)\n"
        f"Feijão Total: {x2_opt*1000:,.0f} kg\n"
        f"Traseiro: 80.000 kg Arroz\n"
        f"Dianteiro: 5.000 kg Arroz + 61.667 kg Feijão\n"
        f"Lucro Máx: R$ {z_opt:,.2f}",
        xy=(x1_opt, x2_opt),
        xytext=(15, 10),
        textcoords="offset points",
        fontsize=9,
        fontweight="bold",
        color="darkred",
        bbox=dict(
            boxstyle="round,pad=0.4", fc="mistyrose", ec="crimson", alpha=0.9
        ),
        arrowprops=dict(arrowstyle="->", color="darkred", lw=1.5),
    )

    ax.set_xlim(-5, 105)
    ax.set_ylim(-5, 125)
    ax.set_xlabel(r"Arroz Total Transportado ($x_1$) [toneladas]", fontsize=11)
    ax.set_ylabel(r"Feijão Total Transportado ($x_2$) [toneladas]", fontsize=11)
    ax.set_title(
        r"Otimização da Carga do Trem — Região Viável e Alocação Ótima",
        fontsize=13,
        pad=14,
    )
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.legend(loc="upper right", framealpha=0.92, fontsize=8.5)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    plotar_otimizacao_trem()