"""
Otimização de Produção de Medicamentos (Saracura Produtos Farmacêuticos)
Determinação dos pontos extremos e resolução gráfica via SciPy (HiGHS) e Matplotlib.

Problema:
    Max Z = 5*x1 + 8*x2
    sujeito a:
        1*x1 + 4*x2 <= 8   (Matéria-prima A)
        1*x1 + 1*x2 <= 5   (Matéria-prima B)
        x1, x2 >= 0
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import linprog


def resolver_saracura():
    # linprog minimiza: Max Z <=> Min (-Z)
    c = [-5.0, -8.0]

    A_ub = [
        [1.0, 4.0],  # Matéria-prima A
        [1.0, 1.0],  # Matéria-prima B
    ]
    b_ub = [8.0, 5.0]

    bounds = [(0.0, None), (0.0, None)]

    res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs")

    if not res.success:
        raise RuntimeError(f"Falha na resolução do modelo: {res.message}")

    return {
        "analgesico": float(res.x[0]),
        "antibiotico": float(res.x[1]),
        "receita_max": float(-res.fun),
    }


def plotar_grafico(solucao):
    x1_opt = solucao["analgesico"]
    x2_opt = solucao["antibiotico"]
    z_opt = solucao["receita_max"]

    # Malha para o plano cartesiano (em toneladas)
    x1_vals = np.linspace(0, 9, 1000)
    x2_vals = np.linspace(0, 6, 1000)
    X1, X2 = np.meshgrid(x1_vals, x2_vals)

    # Fronteiras isolando x2:
    # Reta A: 1*x1 + 4*x2 = 8 => x2 = (8 - x1)/4 = 2 - 0.25*x1
    r_mat_a = (8.0 - x1_vals) / 4.0

    # Reta B: 1*x1 + 1*x2 = 5 => x2 = 5 - x1
    r_mat_b = 5.0 - x1_vals

    fig, ax = plt.subplots(figsize=(10, 7))

    # Curvas de restrição
    ax.plot(
        x1_vals,
        np.maximum(0, r_mat_a),
        label=r"Matéria-prima A: $x_1 + 4x_2 \leq 8$ t",
        color="royalblue",
        linewidth=2,
    )
    ax.plot(
        x1_vals,
        np.maximum(0, r_mat_b),
        label=r"Matéria-prima B: $x_1 + x_2 \leq 5$ t",
        color="darkorange",
        linewidth=2,
    )

    # Região factível (área sombreada)
    regiao_factivel = (
        (X1 + 4.0 * X2 <= 8.0)
        & (X1 + X2 <= 5.0)
        & (X1 >= 0)
        & (X2 >= 0)
    )

    ax.imshow(
        regiao_factivel.astype(int),
        extent=(0, 9, 0, 6),
        origin="lower",
        cmap="Greens",
        alpha=0.25,
    )

    # Retas da Função-Objetivo (Isoreceita: 5x1 + 8x2 = Z => x2 = - (5/8)x1 + Z/8)
    # 1. Reta intermediária
    z_inter = 16.0
    ax.plot(
        x1_vals,
        -(5.0 / 8.0) * x1_vals + z_inter / 8.0,
        color="crimson",
        linestyle=":",
        alpha=0.6,
        label=rf"F.O. $Z = \text{{R\$\,}}{z_inter:.2f}$",
    )

    # 2. Reta no ponto ótimo (último contato com a região factível)
    ax.plot(
        x1_vals,
        -(5.0 / 8.0) * x1_vals + z_opt / 8.0,
        color="crimson",
        linewidth=2.5,
        label=rf"F.O. Ótima $Z^* = \text{{R\$\,}}{z_opt:.2f}$",
    )

    # Vértices (Pontos Extremos)
    vertices = {
        r"$V_1(0; 0)$": (0.0, 0.0),
        r"$V_2(0; 2)$": (0.0, 2.0),
        r"$V_4(5; 0)$": (5.0, 0.0),
    }

    for rotulo, (vx, vy) in vertices.items():
        z_v = 5.0 * vx + 8.0 * vy
        ax.plot(vx, vy, "ko", markersize=6)
        ax.annotate(
            f"{rotulo}\n[Z = R$ {z_v:.0f}]",
            (vx, vy),
            textcoords="offset points",
            xytext=(10, 5),
            fontsize=9,
        )

    # Ponto ótimo destacado
    ax.plot(
        x1_opt,
        x2_opt,
        "ro",
        markersize=10,
        label=rf"Ótimo $V_3({x1_opt:.0f};\, {x2_opt:.0f})$ [$Z^*=\text{{R\$\,}}{z_opt:.2f}$]",
    )
    ax.annotate(
        f"$V_3(4; 1)$ - ÓTIMO\n[Z = R$ {z_opt:.0f}]",
        (x1_opt, x2_opt),
        textcoords="offset points",
        xytext=(10, 10),
        fontsize=10,
        fontweight="bold",
        color="darkred",
    )

    # Vetor de direção de crescimento da receita (Gradiente = [5, 8])
    ax.annotate(
        "Sentido de Maximização (Crescimento de Z)",
        xy=(x1_opt, x2_opt),
        xytext=(x1_opt + 1.5, x2_opt + 2.0),
        arrowprops=dict(
            facecolor="crimson", shrink=0.08, width=1.5, headwidth=8
        ),
        fontsize=10,
        fontweight="bold",
        color="darkred",
    )

    ax.set_xlim(0, 8.5)
    ax.set_ylim(0, 5.5)
    ax.set_xlabel(r"Analgésico ($x_1$) [toneladas]", fontsize=12)
    ax.set_ylabel(r"Antibiótico ($x_2$) [toneladas]", fontsize=12)
    ax.set_title(
        r"Indústrias Saracura — Maximização da Receita ($\max Z = 5x_1 + 8x_2$)",
        fontsize=13,
        pad=15,
    )
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.legend(loc="upper right", framealpha=0.92, fontsize=9)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    sol = resolver_saracura()
    print("=" * 52)
    print("   SARACURA PRODUTOS FARMACÊUTICOS — PLANO ÓTIMO    ")
    print("=" * 52)
    print(f"Analgésico a produzir (x1*) : {sol['analgesico']:.1f} toneladas")
    print(f"Antibiótico a produzir (x2*): {sol['antibiotico']:.1f} toneladas")
    print("-" * 52)
    print(f"Receita Máxima Diária (Z*)  : R$ {sol['receita_max']:,.2f}")
    print("=" * 52)

    plotar_grafico(sol)