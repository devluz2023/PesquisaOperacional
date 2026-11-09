"""
Otimização de Transporte de Cargas (Deixa Comigo S.A.)
Maximização de lucro via SciPy (HiGHS) e plotagem gráfica da região viável.

Problema:
    Max Z = 0.12*x1 + 0.35*x2
    sujeito a:
        x1 + x2 <= 70.000             (Capacidade de Peso em kg)
        0.4*x1 + 0.2*x2 <= 30.000     (Capacidade de Volume em m³)
        x1 <= 100.000                 (Demanda/Disponibilidade de Sementes)
        x2 <= 85.000                  (Demanda/Disponibilidade de Grãos)
        x1, x2 >= 0
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import linprog


def resolver_transporte():
    # Max Z <=> Min (-Z) no linprog
    c = [-0.12, -0.35]

    # Matriz das inequações (A_ub @ x <= b_ub)
    A_ub = [
        [1.0, 1.0],  # Peso
        [0.4, 0.2],  # Volume
    ]
    b_ub = [70000.0, 30000.0]

    # Limites individuais das variáveis (não-negatividade e demanda máxima)
    bounds = [(0.0, 100000.0), (0.0, 85000.0)]

    res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs")

    if not res.success:
        raise RuntimeError(f"Falha na convergência do solver: {res.message}")

    return {
        "x1": float(res.x[0]),
        "x2": float(res.x[1]),
        "lucro_max": float(-res.fun),
    }


def plotar_grafico(solucao):
    x1_opt = solucao["x1"]
    x2_opt = solucao["x2"]
    z_opt = solucao["lucro_max"]

    # Malha para o plano cartesiano (em milhares de kg)
    x1_vals = np.linspace(0, 110000, 1000)
    x2_vals = np.linspace(0, 100000, 1000)
    X1, X2 = np.meshgrid(x1_vals, x2_vals)

    # Fronteiras isolando x2:
    # 1. Peso: x1 + x2 = 70.000 => x2 = 70.000 - x1
    r_peso = 70000.0 - x1_vals

    # 2. Volume: 0.4*x1 + 0.2*x2 = 30.000 => x2 = (30.000 - 0.4*x1) / 0.2 = 150.000 - 2*x1
    r_volume = (30000.0 - 0.4 * x1_vals) / 0.2

    fig, ax = plt.subplots(figsize=(11, 7))

    # Plot das retas de restrição
    ax.plot(
        x1_vals / 1000,
        np.maximum(0, r_peso) / 1000,
        label=r"Peso: $x_1 + x_2 \leq 70.000$ kg (Ativa)",
        color="royalblue",
        linewidth=2.2,
    )
    ax.plot(
        x1_vals / 1000,
        np.maximum(0, r_volume) / 1000,
        label=r"Volume: $0{,}4x_1 + 0{,}2x_2 \leq 30.000$ $\text{m}^3$ (Redundante)",
        color="gray",
        linestyle="--",
        linewidth=1.8,
    )
    ax.axvline(
        100,
        color="tab:purple",
        linestyle=":",
        linewidth=1.5,
        label=r"Demanda Sementes: $x_1 \leq 100.000$ kg",
    )
    ax.axhline(
        85,
        color="tab:orange",
        linestyle=":",
        linewidth=1.5,
        label=r"Demanda Grãos: $x_2 \leq 85.000$ kg",
    )

    # Região factível
    regiao_factivel = (
        (X1 + X2 <= 70000.0)
        & (0.4 * X1 + 0.2 * X2 <= 30000.0)
        & (X1 <= 100000.0)
        & (X2 <= 85000.0)
        & (X1 >= 0)
        & (X2 >= 0)
    )

    ax.imshow(
        regiao_factivel.astype(int),
        extent=(0, 110, 0, 100),
        origin="lower",
        cmap="Greens",
        alpha=0.25,
    )

    # Retas da Função-Objetivo (Isolucro: 0.12*x1 + 0.35*x2 = Z => x2 = -(12/35)*x1 + Z/0.35)
    # 1. Reta intermediária
    z_inter = 12000.0
    ax.plot(
        x1_vals / 1000,
        (-(0.12 / 0.35) * x1_vals + z_inter / 0.35) / 1000,
        color="crimson",
        linestyle=":",
        alpha=0.6,
        label=rf"F.O. $Z = \text{{R\$\,}}{z_inter:,.0f}$",
    )

    # 2. Reta no ponto ótimo (último contato antes de sair da região viável)
    ax.plot(
        x1_vals / 1000,
        (-(0.12 / 0.35) * x1_vals + z_opt / 0.35) / 1000,
        color="crimson",
        linewidth=2.5,
        label=rf"F.O. Ótima $Z^* = \text{{R\$\,}}{z_opt:,.2f}$",
    )

    # Vértices da região viável
    ax.plot(0, 0, "ko", markersize=5)
    ax.plot(70, 0, "ko", markersize=6, label=r"Vértice $(70.000;\, 0)$ [$Z = \text{R\$\,8.400}$]")

    # Ponto ótimo destacado
    ax.plot(
        x1_opt / 1000,
        x2_opt / 1000,
        "ro",
        markersize=9,
        label=rf"Ótimo $({x1_opt:,.0f};\, {x2_opt:,.0f})$ [$Z^* = \text{{R\$\,}}{z_opt:,.2f}$]",
    )

    # Vetor indicando a direção de maximização
    ax.annotate(
        "Sentido de Maximização (Crescimento de Z)",
        xy=(0, 70),
        xytext=(20, 85),
        arrowprops=dict(
            facecolor="crimson", shrink=0.08, width=1.5, headwidth=8
        ),
        fontsize=10,
        fontweight="bold",
        color="darkred",
    )

    ax.set_xlim(0, 110)
    ax.set_ylim(0, 100)
    ax.set_xlabel(r"Sementes ($x_1$) [milhares de kg]", fontsize=12)
    ax.set_ylabel(r"Grãos ($x_2$) [milhares de kg]", fontsize=12)
    ax.set_title(
        r"Deixa Comigo S.A. — Maximização de Lucro no Transporte ($\max Z = 0{,}12x_1 + 0{,}35x_2$)",
        fontsize=13,
        pad=15,
    )
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.legend(loc="upper right", framealpha=0.9, fontsize=9)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    resultado = resolver_transporte()
    print("=" * 48)
    print("      DEIXA COMIGO S.A. — RESULTADO ÓTIMO       ")
    print("=" * 48)
    print(f"Carga de Sementes (x1*) : {resultado['x1']:>10,.2f} kg")
    print(f"Carga de Grãos    (x2*) : {resultado['x2']:>10,.2f} kg")
    print(f"Lucro Máximo      (Z*)  : R$ {resultado['lucro_max']:>10,.2f}")
    print("=" * 48)

    plotar_grafico(resultado)