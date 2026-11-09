"""
otimizacao_cat_without_fat.py
-----------------------------
Otimização da mistura de ração para gatos (Cat Without Fat S.A.)
Resolução analítica/gráfica e visualização dos pontos extremos no segmento viável.
"""

import matplotlib.pyplot as plt
import numpy as np


def resolver_e_plotar():
    # Modelagem:
    # x1: fração de frango (0 <= x1 <= 1)
    # x2 = 1 - x1 (fração de peixe)
    # Custo: Z = 3*x1 + 5*(1 - x1) = 5 - 2*x1
    # Gordura: 0.25*x1 + 0.10*(1 - x1) <= 0.15 => 0.15*x1 <= 0.05 => x1 <= 1/3

    x1_range = np.linspace(0, 1, 500)
    gordura = 0.25 * x1_range + 0.10 * (1 - x1_range)
    custo = 3.00 * x1_range + 5.00 * (1 - x1_range)

    # Pontos Extremos
    # Ponto A: x1 = 0 (100% Peixe)
    pt_a_x1 = 0.0
    pt_a_custo = 3.00 * pt_a_x1 + 5.00 * (1.0 - pt_a_x1)
    pt_a_gordura = 0.25 * pt_a_x1 + 0.10 * (1.0 - pt_a_x1)

    # Ponto B: x1 = 1/3 (Ótimo: 33.33% Frango, 66.67% Peixe)
    pt_b_x1 = 1 / 3
    pt_b_custo = 3.00 * pt_b_x1 + 5.00 * (1.0 - pt_b_x1)
    pt_b_gordura = 0.25 * pt_b_x1 + 0.10 * (1.0 - pt_b_x1)

    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Curva de Custo (Eixo Y à esquerda)
    linha_custo = ax1.plot(
        x1_range * 100,
        custo,
        color="crimson",
        linewidth=2.2,
        label="Custo por kg (R$)",
    )
    ax1.set_xlabel("Fração de Frango no Mix (%)", fontsize=11)
    ax1.set_ylabel("Custo por kg (R$)", color="crimson", fontsize=11)
    ax1.tick_params(axis="y", labelcolor="crimson")
    ax1.set_ylim(2.5, 5.5)

    # Curva de Gordura (Eixo Y à direita)
    ax2 = ax1.twinx()
    linha_gordura = ax2.plot(
        x1_range * 100,
        gordura * 100,
        color="royalblue",
        linestyle="--",
        linewidth=2,
        label="Teor de Gordura (%)",
    )
    ax2.set_ylabel("Gordura na Mistura (%)", color="royalblue", fontsize=11)
    ax2.tick_params(axis="y", labelcolor="royalblue")
    ax2.set_ylim(8, 26)

    # Limite máximo de 15% de gordura
    ax2.axhline(15, color="gray", linestyle=":", linewidth=1.5, alpha=0.8)
    ax2.text(
        55,
        15.3,
        "Limite Máximo de Gordura (15%)",
        color="dimgray",
        fontsize=9.5,
    )

    # Destaque da Região Viável (0% a 33.33% de frango)
    ax1.axvspan(
        0,
        (1 / 3) * 100,
        color="mediumseagreen",
        alpha=0.18,
        label="Região Viável (Gordura $\\leq$ 15%)",
    )

    # Marcação dos Pontos Extremos
    # Ponto A
    ax1.plot(pt_a_x1 * 100, pt_a_custo, "ko", markersize=7)
    ax1.annotate(
        f"Ponto A (Apenas Peixe)\nFrango: 0% | Custo: R$ {pt_a_custo:.2f}",
        xy=(pt_a_x1 * 100, pt_a_custo),
        xytext=(15, -15),
        textcoords="offset points",
        fontsize=9,
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.9),
    )

    # Ponto B (ÓTIMO)
    ax1.plot(pt_b_x1 * 100, pt_b_custo, "ro", markersize=9)
    ax1.annotate(
        f"Ponto B (ÓTIMO)\nFrango: {pt_b_x1*100:.2f}% | Peixe: {(1-pt_b_x1)*100:.2f}%\nCusto Mínimo: R$ {pt_b_custo:.2f}/kg",
        xy=(pt_b_x1 * 100, pt_b_custo),
        xytext=(20, 15),
        textcoords="offset points",
        arrowprops=dict(
            arrowstyle="->", connectionstyle="arc3,rad=.2", color="darkred"
        ),
        fontweight="bold",
        color="darkred",
        bbox=dict(
            boxstyle="round,pad=0.4", fc="mistyrose", ec="crimson", alpha=0.9
        ),
    )

    # Legendas combinadas
    linhas = linha_custo + linha_gordura
    rotulos = [l.get_label() for l in linhas]
    ax1.legend(
        linhas + [ax1.get_children()[0]],
        rotulos + ["Região Viável ($\\leq$ 15% Gordura)"],
        loc="upper right",
        framealpha=0.9,
    )

    plt.title(
        "Cat Without Fat S.A. — Otimização Linear da Mistura de Ração",
        fontsize=13,
        pad=15,
    )
    ax1.grid(True, linestyle=":", alpha=0.5)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    resolver_e_plotar()