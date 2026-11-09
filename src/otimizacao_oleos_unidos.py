"""
otimizacao_oleos_unidos.py
--------------------------
Otimização da produção de combustíveis especiais (Óleos Unidos S.A.).
Como x1 = 0 no ponto ótimo, a visualização gráfica no plano (x2, x3)
ilustra o trade-off entre os combustíveis B e C, as restrições de insumos
e a determinação da solução ótima (x3 = 30 unidades / 180 litros).
"""

import matplotlib.pyplot as plt
import numpy as np


def plotar_otimizacao_oleos():
    # Com x1 = 0 (Combustível A não produzido), analisamos o plano (x2, x3)
    # x2: unidades de Combustível B
    # x3: unidades de Combustível C

    x2_vals = np.linspace(0, 35, 400)

    # Fronteiras isolando x3:
    # 1. Extrato Mineral: 5*x2 + 4*x3 <= 120  =>  x3 = (120 - 5*x2) / 4
    r_extrato = (120.0 - 5.0 * x2_vals) / 4.0

    # 2. Solvente: 4*x2 + 2*x3 <= 200  =>  x3 = (200 - 4*x2) / 2
    r_solvente = (200.0 - 4.0 * x2_vals) / 2.0

    fig, ax = plt.subplots(figsize=(10, 7))

    # Curvas de restrição
    ax.plot(
        x2_vals,
        r_extrato,
        label=r"Extrato Mineral: $5x_2 + 4x_3 \leq 120$ (Ativa, folga = 0 L)",
        color="royalblue",
        linewidth=2.2,
    )
    ax.plot(
        x2_vals,
        r_solvente,
        label=r"Solvente: $4x_2 + 2x_3 \leq 200$ (Folga: 140 L)",
        color="darkorange",
        linestyle="--",
        linewidth=2,
    )

    # Região factível no primeiro quadrante (triângulo delimitado pelo extrato)
    # Vértices: (0, 0), (24, 0) [120/5], (0, 30) [120/4]
    pontos_poligono = np.array([[0, 0], [24, 0], [0, 30]])
    poligono = plt.Polygon(
        pontos_poligono,
        closed=True,
        color="mediumseagreen",
        alpha=0.25,
        label="Região Viável ($x_1 = 0$)",
    )
    ax.add_patch(poligono)

    # Isocurvas da Função-Objetivo (Z = 22*x2 + 18*x3 => x3 = (Z - 22*x2)/18)
    z_sub = 360.0
    r_z_sub = (z_sub - 22.0 * x2_vals) / 18.0
    ax.plot(
        x2_vals,
        r_z_sub,
        color="crimson",
        linestyle=":",
        alpha=0.6,
        label=rf"F.O. Sub-ótima ($Z = \mathrm{{R\$}}\,{z_sub:.0f}$)",
    )

    z_opt = 540.0
    r_z_opt = (z_opt - 22.0 * x2_vals) / 18.0
    ax.plot(
        x2_vals,
        r_z_opt,
        color="crimson",
        linewidth=2.4,
        label=rf"F.O. Ótima ($Z^* = \mathrm{{R\$}}\,{z_opt:.0f}$)",
    )

    # Marcação dos vértices
    vertices = {
        r"$V_1(0; 0)$": (0, 0),
        r"$V_2(24; 0)$": (24, 0),
    }

    for rotulo, (vx, vy) in vertices.items():
        z_v = 22 * vx + 18 * vy
        ax.plot(vx, vy, "ko", markersize=6)
        ax.annotate(
            f"{rotulo}\n[R$ {z_v:.0f}]",
            (vx, vy),
            textcoords="offset points",
            xytext=(8, 6),
            fontsize=9,
        )

    # Ponto Ótimo: (x2=0, x3=30)
    x2_opt, x3_opt = 0.0, 30.0
    ax.plot(
        x2_opt,
        x3_opt,
        "ro",
        markersize=9,
        label=rf"Ótimo $V_3(x_2=0;\, x_3=30)$",
    )
    ax.annotate(
        f"$V_3(0; 30)$ — ÓTIMO\nComb. C: 30 unids (180 L)\nExtrato Usado: 120 L (100%)\nSobra de Solvente: 140 L\nLucro Máx: R$ {z_opt:,.2f}",
        (x2_opt, x3_opt),
        textcoords="offset points",
        xytext=(15, -15),
        fontsize=9.5,
        fontweight="bold",
        color="darkred",
        bbox=dict(
            boxstyle="round,pad=0.4", fc="mistyrose", ec="crimson", alpha=0.9
        ),
        arrowprops=dict(arrowstyle="->", color="darkred", lw=1.5),
    )

    ax.set_xlim(-1, 32)
    ax.set_ylim(-1, 45)
    ax.set_xlabel(r"Unidades de Combustível B ($x_2$)", fontsize=11)
    ax.set_ylabel(r"Unidades de Combustível C ($x_3$)", fontsize=11)
    ax.set_title(
        r"Óleos Unidos S.A. — Otimização Linear e Região Viável ($x_1 = 0$)",
        fontsize=13,
        pad=14,
    )
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.legend(loc="upper right", framealpha=0.92, fontsize=8.5)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    plotar_otimizacao_oleos()